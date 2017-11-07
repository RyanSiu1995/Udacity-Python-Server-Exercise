#!/usr/bin/env python
from BaseHTTPServer import HTTPServer
from handler import WebSeverHandler


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebSeverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print "Stopping the server"
        server.socket.close()

if __name__ == "__main__":
    main()
