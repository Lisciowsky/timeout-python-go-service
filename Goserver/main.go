package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"time"
)

type application struct {
	logger *log.Logger
}

type AppStatus struct {
	Status      string `json:"status"`
	Environment string `json:"environment"`
	Version     string `json:"version"`
}

func main() {
	logger := log.New(os.Stdout, "", log.Ldate|log.Ltime)

	app := &application{logger: logger}
	srv := &http.Server{
		Addr:         fmt.Sprintf(":%d", 8000),
		Handler:      app.routes(),
		IdleTimeout:  time.Minute,
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 30 * time.Second,
	}

	err := srv.ListenAndServe()
	if err != nil {
		log.Println(err)
	}
}
