
'''
from http.server import HTTPServer, BaseHTTPRequestHandler
from time import sleep

index_html = open('index.html', 'r').read()

class handlerRequest(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        # send an html file that will call
        # another route to listen for chords
        counter = 0
        while True:
            self.wfile.write(str(counter).encode())
            counter += 1
            sleep(60)
        


def main():
    PORT = 8000
    server = HTTPServer(('', PORT), handlerRequest)
    print('Server ran on port', PORT)
    server.serve_forever()

if __name__ == '__main__':
    main()
'''

'''
import socket


# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

while True:    
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # Get the client request
    request = client_connection.recv(1024).decode()
    print(request)

    # Get the content of htdocs/index.html
    fin = open('index.html')
    content = fin.read()
    fin.close()

    # Send HTTP response
    response = 'HTTP/1.0 200 OK\n\n' + content
    client_connection.sendall(response.encode())
    client_connection.close()

# Close socket
server_socket.close()

# https://www.codementor.io/@joaojonesventura/building-a-basic-http-server-from-scratch-in-python-1cedkg0842
'''

from flask import Flask, render_template, request, g, session
import hashlib

app = Flask(__name__)
app.secret_key = "some random key"

# def get_chord():
#     print('chord' not in session.keys())
#     if 'chord' not in session.keys():
#         print('Hi')
#         print(session.keys())
#         set_chord({'key': 'Nne', 'notes': []})

#     return session['chord']

# def set_chord(chord):
#     session['chord'] = chord
#     session.modified = True

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/chord', methods=['POST', 'GET'])
def chord():
    if request.method == 'POST':
        # set_chord(request.json)
        session['chord'] = request.json
        return 'good'
    else:
        print(session.new)
        chord = session['chord'] 
        return chord


if __name__ == '__main__':
    app.run()