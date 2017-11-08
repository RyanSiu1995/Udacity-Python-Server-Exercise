#!/usr/bin/env python
from BaseHTTPServer import HTTPServer
from WebServerSetting import app


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
