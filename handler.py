#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler
import cgi


class WebSeverHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                output = ""
                output += "<html><body>Hello!"
                output += """
                <form method='POST' enctype='multipart/form-data'
                action='/hello'><h2>What would you want to say?</h2>
                <input name='message' type='text'><input type='submit'
                value='Submit'></form>"""
                output += "</body></html>"
                self.wfile.write(output)
                return
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                output = ""
                output += "<html><body>&#161hola!" + \
                    "<a href='/hello'>back to hello</a></body></html>"
                self.wfile.write(output)
                return
        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()

            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

            output = ""
            output += "<html><body>"
            output += "<h2>Data recieved:</h2>"
            output += "<h1>%s<h1>" % messagecontent
            output += """
                <form method='POST' enctype='multipart/form-data'
                action='/hello'><h2>What would you want to say?</h2>
                <input name='message' type='text'><input type='submit'
                value='Submit'></form>"""
            output += "</body></html>"
            self.wfile.write(output)
        except:
            pass
