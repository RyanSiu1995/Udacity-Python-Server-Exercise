#!/usr/bin/env python
from BaseHTTPServer import HTTPServer
from webServerSetting import app


if __name__ == "__main__":
	# Run the server in port 5000
    app.run(host="0.0.0.0", port=5000)
