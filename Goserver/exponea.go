package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
	"time"
)

type RequestTimeout struct {
	Timeout time.Duration `json:"timeout"`
}

const URL string = "https://exponea-engineering-assignment.appspot.com/api/work"

func (app *application) statusHandler(w http.ResponseWriter, r *http.Request) {
	currentStatus := AppStatus{
		Status:      "Available",
		Environment: "Test",
		Version:     "0.01",
	}

	js, err := json.MarshalIndent(currentStatus, "", "")
	if err != nil {
		app.logger.Println(err)
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	w.Write(js)
}

func makesfakerequest(timeout time.Duration, success bool) (int, error) {
	// fmt.Println("Sleeping for one second -> TODO REMOVE ME")
	time.Sleep(50 * time.Millisecond)
	if success {
		return 200, nil
	}
	return 400, nil
}

func concurrentRequest(status chan int, done chan bool, timeout time.Duration, success bool) {
	select {
	case <-done:
		return
	default:
		statusCode, err := sendRequest(URL)
		// statusCode, err := makesfakerequest(timeout, success)
		// fmt.Printf("Called url, status code: %v \n", statusCode)
		if err != nil || statusCode == 0 {
			statusCode = 400
		}
		status <- statusCode
	}

}

func spinTwoGoRequests(ch chan int, success chan bool, done chan bool, failesLimit int) {
	select {
	case <-done:
		return
	default:
		go concurrentRequest(ch, done, 1, false)
		go concurrentRequest(ch, done, 1, true)

		var fails int
		for s := range ch {
			if s == 200 {
				success <- true
				return
			}
			fails++
			if fails == failesLimit {
				success <- false
				return
			}
		}
	}

}

func (app *application) getExponsaRequests(w http.ResponseWriter, r *http.Request) {
	// 1) we need to use the req.timeout given from the client as a global timeout for all of the requests.
	// 2) We need spin FIRST request with given timeout of 300 milisecond.
	//    - if there is no response OR response.statusCode != 200 THEN we need to spin another goroutines.
	//    - if there is response and response.statusCode == 200 THEN we return the response back to client.
	// Optional *3) After 3 goroutines are running we have to check periodically if they return valid response and status code.
	// 				If any does return, we FINISH.
	app.logger.Println("----New-Post-Request----")
	var req RequestTimeout
	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		app.errorJSON(w, errors.New("Unable to parse the request body..."))
	}
	isGlobalTimeout := make(chan bool)

	go func() {
		app.logger.Printf("Setting global timeout with: %v milisecond", req.Timeout)
		time.Sleep(req.Timeout * time.Millisecond)
		isGlobalTimeout <- true
	}()

	ch := make(chan int)
	success := make(chan bool)

	app.logger.Println("Calling first request")
	go concurrentRequest(ch, isGlobalTimeout, 1, false)
	// just looking just a sec
	select {
	case s := <-ch:
		app.logger.Printf("First request: received value %v", s)
		if s == 200 {
			app.logger.Printf("First request: status code 200. returning response with timeout: %v", req.Timeout)
			app.writeJSON(w, 200, req.Timeout, "timeout")
			return
		}
		app.logger.Printf("First request: status code != 200, spinning another gorutines...")
		go spinTwoGoRequests(ch, success, isGlobalTimeout, 2)

	case <-time.After(300 * time.Millisecond):
		fmt.Println("timeout 1")
		app.logger.Printf("First request 300 milisecond timeout, spinning another gorutines...")

		go spinTwoGoRequests(ch, success, isGlobalTimeout, 3)

	case <-isGlobalTimeout:
		app.logger.Println("Global timeout exhaused, stopping... ")
		app.errorJSON(w, errors.New("Global timeout exhausted."))
		return

	}

	select {
	case succeed := <-success:
		fmt.Println("Success channel response...")
		if succeed == true {
			fmt.Println("Gorutine returned successful status code: 200")
			app.writeJSON(w, 200, req.Timeout, "timeout")
			return
		}
		fmt.Println("Gorutine returned ")
		app.errorJSON(w, errors.New("All requests has returned wrong status code..."))
		return

	case <-isGlobalTimeout:
		app.logger.Println("Global timeout exhaused, stopping... ")
		app.errorJSON(w, errors.New("Global timeout exhausted."))
		return
	}
}

func sendRequest(url string) (int, error) {
	resp, err := http.Get(url)
	if err != nil {
		return 0, err
	}
	return resp.StatusCode, nil
}
