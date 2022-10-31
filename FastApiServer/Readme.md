PYTHON FASTAPI SERVER

10000 Requests in Total 100 simultaneously at the same time. body = {"timeout": 2500}

ab -c 100 -n 10000 -p body.json http://127.0.0.1:8000/api/smart

TEST_SETUP:

- 50 miliseconds for each (Dummy/Fake -> makesfakerequest function) request
- first request fails
- second request fails
- third request succeeds

Server Software: uvicorn
Server Hostname: 127.0.0.1
Server Port: 8000

Document Path: /api/smart
Document Length: 16 bytes

Concurrency Level: 100
Time taken for tests: 12.565 seconds
Complete requests: 10000
Failed requests: 0
Total transferred: 1600000 bytes
Total body sent: 1580000
HTML transferred: 160000 bytes
Requests per second: 795.84 [#/sec] (mean)
Time per request: 125.654 [ms] (mean)
Time per request: 1.257 [ms] (mean, across all concurrent requests)
Transfer rate: 124.35 [Kbytes/sec] received
122.80 kb/s sent
247.14 kb/s total

Connection Times (ms)
min mean[+/-sd] median max
Connect: 0 0 0.3 0 4
Processing: 102 124 17.6 119 224
Waiting: 102 122 16.7 118 224
Total: 102 124 17.7 119 224

Percentage of the requests served within a certain time (ms)
50% 119
66% 125
75% 130
80% 133
90% 144
95% 157
98% 183
99% 203
100% 224 (longest request)

---

# ! NOTE !

# Result from Calling Exponea server directly below.

ab -c 100 -n 1000 -p body.json http://127.0.0.1:80/api/smart
1000 requests 100 concurrent

Server Software: uvicorn
Server Hostname: 127.0.0.1
Server Port: 8000

Document Path: /api/smart
Document Length: 16 bytes

Concurrency Level: 100
Time taken for tests: 30.896 seconds
Complete requests: 1000
Failed requests: 999
(Connect: 0, Receive: 0, Length: 999, Exceptions: 0)
Total transferred: 173986 bytes
Total body sent: 158000
HTML transferred: 29986 bytes
Requests per second: 32.37 [#/sec] (mean)
Time per request: 3089.622 [ms] (mean)
Time per request: 30.896 [ms] (mean, across all concurrent requests)
Transfer rate: 5.50 [Kbytes/sec] received
4.99 kb/s sent
10.49 kb/s total

Connection Times (ms)
min mean[+/-sd] median max
Connect: 0 1 1.0 0 5
Processing: 2254 2552 665.1 2515 23527
Waiting: 2248 2549 665.0 2513 23527
Total: 2254 2552 665.1 2516 23527
WARNING: The median and mean for the initial connection time are not within a normal deviation
These results are probably not that reliable.

Percentage of the requests served within a certain time (ms)
50% 2516
66% 2523
75% 2538
80% 2549
90% 2599
95% 2602
98% 2665
99% 2691
100% 23527 (longest request)
