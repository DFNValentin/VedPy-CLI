from http.server import HTTPServer, SimpleHTTPRequestHandler
import os


os.chdir('./web')
httpd = HTTPServer(('localhost', 8050), SimpleHTTPRequestHandler)
httpd.serve_forever()
