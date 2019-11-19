# SimpleProxyProject
A very simple HTTP proxy that places JWT headers into POST requests

The proxy will only handle POST and GET requests. 
GET request simply returns a string "Nothing done"
POST requests will add a JWT header and relay POST request to the upstream endpoint and returns the reponse from upstream server.


Run using python3.x:
python3 SimpleProxy.py [<local-port> [<dest-url]]>
  
Where:
<local-port> (optional) is the local netowrk port that SimpleProxy will linsten on
<dest-url> (optional) is the upstream endpoint URL (defaults to "http://postman-echo.com/post"


Dependancies:
Standard python libraries:
sys, os, socket, threading, json, datetime, uuid, http.server
Other python libraries:
reuests, pyjwt
  
Security:
This is a very simple test application not intended to be used in production.
