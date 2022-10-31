This repo contains two services, first written in Go another written in Python.
The idea is that the services are calling unstable server (varied response time, no response time / crash), given the timeout as parameter in http post body request.

If the call runtime exceedes timeout, the service will not wait for the responsefrom unstable XYZ server.

For the sake of speed comparision between the two services, inside the repo's readme files, I have recorded the apache benchmark server results (AB test).
To obtain the same scenario for both (Go and Python) web serwers, the XYZ serwerresponses were mocked.
