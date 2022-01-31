# Reference Code: https://github.com/jihoonog/CMPUT404-assignment-webserver/blob/master/server.py

#  coding: utf-8 
import socketserver, os, time, mimetypes

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        request = self.request.recv(1024).decode().strip().split()
        request_type = request[0]
        request_path = request[1] 

        path = "./www" + request_path
        if request_path.endswith("/"):
            path = path + "index.html"


        if request_type != "GET":
            response = "HTTP/1.1 405 Method Not Allowed\r\nDate: {0}\r\nServer: 404asn1 server\r\nAllow: GET\r\n\r\n".format(str(time.ctime()))
            self.request.sendall(response.encode())

        elif "../" in path:
            content_type = mimetypes.guess_type(path)[0]
            response_header = "HTTP/1.1 404 Not Found\r\nDate: {0}\r\nServer: 404asn1 server\r\nContent-Type: {1}\r\nContent-Length: {2}\r\n\r\n".format(str(time.ctime()), content_type, 0)
            self.request.sendall(response_header.encode())
        
        else:
            try:
                file = open(path, "rb")
                response_body = file.read()
                content_type = mimetypes.guess_type(path)[0]
                response_header = "HTTP/1.1 200 OK\r\nDate: {0}\r\nServer: 404asn1 server\r\nContent-Type: {1}\r\nContent-Length: {2}\r\n\r\n".format(str(time.ctime()), content_type, len(response_body))
                self.request.sendall(response_header.encode())
                self.request.sendall(response_body)
                file.close()

            except IsADirectoryError:
                content_type = mimetypes.guess_type(path)[0]
                response_header = "HTTP/1.1 301 Moved Permanently\r\nDate: {0}\r\nServer: 404asn1 server\r\nContent-Type: {1}\r\nContent-Length: {2}\r\nLocation: {3}\r\n\r\n".format(str(time.ctime()), content_type, 0, "http://127.0.0.1:8080" + request_path + "/")
                self.request.sendall(response_header.encode())

            except FileNotFoundError:
                content_type = mimetypes.guess_type(path)[0]
                response_header = "HTTP/1.1 404 Not Found\r\nDate: {0}\r\nServer: 404asn1 server\r\nContent-Type: {1}\r\nContent-Length: {2}\r\n\r\n".format(str(time.ctime()), content_type, 0)
                self.request.sendall(response_header.encode())


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
