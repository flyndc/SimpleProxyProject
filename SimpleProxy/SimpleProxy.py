# Use python3

# Usage: SimpleProxy.py [<inbound port>[ <outbound url>]]

# TOTDO:
#   ADD HTTPS support for inbound requests
#   Secure key storage and access
#   Enable multithread support
#

import sys, os, socket, threading, json, datetime, uuid, ssl
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import jwt

# Constants
MAX_DATA_RX = 10000
MAX_CONNECTIONS = 25

# Globals
srcPort = None
destAddr = ""
jwtSecret = ""

class RequestHandler(BaseHTTPRequestHandler):

  def do_GET(self):
    self.send_response(501)
    self.end_headers()
    self.wfile.write(('Nothing done').encode())
    return

  def do_POST(self):
    content_len = int(self.headers['Content-Length'])
    srcData = self.rfile.read(content_len)
    self.send_response(200)
    self.end_headers()
    destResponse = self.upstreamRequest(destAddr, srcData)
    try:
      jsonResp = json.loads(destResponse)
      self.wfile.write((jsonResp['data']).encode())
    except Exception as err:
      self.log_error("Response was not a JSON object") # ignore request data that is not a json object 

  def upstreamRequest(self, dest, destData):
    jwtPayload = json.loads('{"user":"username","date":"' + str(datetime.date.today()) + '"}')
    jwtHeader = json.loads('{"iat":"' + str(datetime.datetime.now()) + '", "jti":"' + str(uuid.uuid1()) + '"}')
    token = (jwt.encode(jwtPayload, jwtSecret, algorithm='HS512', headers=jwtHeader)).decode()
    hdrString = '{"Content-type": "application/json", "Authorization": "Bearer ' + token + '"}'
    destHeaders = json.loads(hdrString)
    try:
      r = requests.post(dest, data=destData, headers=destHeaders)
    except  Exception as err:
      self.log_error("Upstream request error: %s", err)
      self.send_error(502, "", "")
      return("{}")
    self.log_message("Upstream request to %s with status : %s", dest, r.status_code)
    return(r.text)

def run():
  global destAddr
  global srcPort
  global jwtSecret
  try:
    f = open("secret.key","r")
    jwtSecret = f.read()
  except Exception as err:
    print("Unable to open file: %s",err)
    exit(1)
  if len(sys.argv) > 2:
    destAddr = sys.argv[2]
  if len(sys.argv) > 1:
    srcPort = int(sys.argv[1])
  if srcPort == None:
    srcPort = 80
  if destAddr == "":
    destAddr = "https://postman-echo.com/post" 
  print("starting ... on port: ", srcPort, " to endpoint ", destAddr)
  httpd = HTTPServer(('localhost', srcPort), RequestHandler)
  httpd.serve_forever()

if __name__ == '__main__':
  run()
