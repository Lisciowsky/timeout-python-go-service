GOLANG NET/HTTP SERVER

10000 Requests in Total 100 simultaneously at the same time. body = {"timeout": 2500}

ab -c 100 -n 10000 -p body.json http://127.0.0.1:8000/api/smart

TEST_SETUP:

- 50 miliseconds for each (Dummy/Fake -> makesfakerequest function) request
- first request fails
- second request fails
- third request succeeds

Server Software:
Server Hostname: 127.0.0.1
Server Port: 8000

Document Path: /api/smart
Document Length: 58 bytes

Concurrency Level: 100
Time taken for tests: 10.378 seconds
Complete requests: 10000
Failed requests: 0
Total transferred: 1980000 bytes
Total body sent: 1580000
HTML transferred: 580000 bytes
Requests per second: 963.60 [#/sec] (mean)
Time per request: 103.778 [ms] (mean)
Time per request: 1.038 [ms] (mean, across all concurrent requests)
Transfer rate: 186.32 [Kbytes/sec] received
148.68 kb/s sent
335.00 kb/s total

Connection Times (ms)
min mean[+/-sd] median max
Connect: 0 1 0.5 0 5
Processing: 100 102 1.7 101 116
Waiting: 100 102 1.7 101 116
Total: 100 102 1.9 102 116
WARNING: The median and mean for the initial connection time are not within a normal deviation
These results are probably not that reliable.

Percentage of the requests served within a certain time (ms)
50% 102
66% 103
75% 103
80% 103
90% 105
95% 106
98% 109
99% 110
100% 116 (longest request)

---

# ! NOTE !

## Below results hitting the actual Exponea server.

ab -c 100 -n 1000 -p body.json http://127.0.0.1:8000/api/smart

1000 requests, 100 concurrent

Concurrency Level: 100
Time taken for tests: 26.526 seconds
Complete requests: 1000
Failed requests: 955
(Connect: 0, Receive: 0, Length: 955, Exceptions: 0)
Non-2xx responses: 955
Total transferred: 198000 bytes
Total body sent: 158000
HTML transferred: 49405 bytes
Requests per second: 37.70 [#/sec] (mean)
Time per request: 2652.605 [ms] (mean)
Time per request: 26.526 [ms] (mean, across all concurrent requests)
Transfer rate: 7.29 [Kbytes/sec] received
5.82 kb/s sent
13.11 kb/s total

Connection Times (ms)
min mean[+/-sd] median max
Connect: 0 1 1.0 0 5
Processing: 466 2456 260.9 2504 2521
Waiting: 465 2456 260.9 2504 2521
Total: 469 2457 260.5 2504 2525
WARNING: The median and mean for the initial connection time are not within a normal deviation
These results are probably not that reliable.

Percentage of the requests served within a certain time (ms)
50% 2504
66% 2504
75% 2505
80% 2506
90% 2510
95% 2515
98% 2520
99% 2522
100% 2525 (longest request)
