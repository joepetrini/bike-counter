echo 'Running on port 1080'
#python -m SimpleHTTPServer 0.0.0.0:1080
python -c 'import BaseHTTPServer as bhs, SimpleHTTPServer as shs; bhs.HTTPServer(("0.0.0.0", 1080), shs.SimpleHTTPRequestHandler).serve_forever()'

