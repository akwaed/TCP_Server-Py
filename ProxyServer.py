from socket import *
import urllib
from urllib.request import Request, urlopen, HTTPError
import argparse
import os

def main():
    # Get port command line argument
    parser = argparse.ArgumentParser()
    # parser.add_argument('port')
    args = parser.parse_args()

    # Define socket host and port
    SERVER_HOST = ''
    SERVER_PORT = 8888

    # Initialize socket
    server_socket = socket(AF_INET, SOCK_STREAM)
    #server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))

    server_socket.listen(1)

    print('Cache proxy is listening on port %s...' % SERVER_PORT)

    while True:
        print('\nProxy is ready to serve...')

        # Wait for client connection
        client_connection, client_address = server_socket.accept()

        # Get the client request
        request = client_connection.recv(1024).decode()
        # print(request)

        # Parse HTTP headers
        headers = request.split('\n')
        print(headers[0])
        top_header = headers[0].split()
        method = top_header[0]
        filename = '/' + top_header[1].split('/')[2]
        serverPath = top_header[1].split('/')[1]
        if(filename.endswith(".jpg")):
            filetype = 'image/jpg'
        if(filename.endswith(".jpeg")):
            filetype = 'image/jpeg'
        elif(filename.endswith(".mp4")):
            filetype = 'video/mp4'
        else:
            filetype = 'text/html'

        # Get the file
        content = fetch_file(filename,filetype,serverPath)

        # If we have the file, return it, otherwise 404
        if content:
            response = 'HTTP/1.0 200 OK\n\n'.encode() + content
        else:
            print('404 File not found on server')
            response = 'HTTP/1.0 404 NOT FOUND\n\n'.encode()

        # Send the response and close the connection
        client_connection.sendall(response)
        client_connection.close()
        # Send the response and close the connection

    # Close socket
    server_socket.close()


def fetch_file(filename, filetype, serverPath):
    # Let's try to read the file locally first
    file_from_cache = fetch_from_cache(filename,filetype)

    if file_from_cache:
        print('Fetched successfully from cache.')
        return file_from_cache
    else:
        print('Not in cache. Fetching from server.')
        file_from_server = fetch_from_server(filename,serverPath)

        if file_from_server:
            print('File found on server')
            save_in_cache(filename, file_from_server)
            return file_from_server
        else:
            return None


def fetch_from_cache(filename,file_type):
    try:
        if(file_type == 'image/jpg'):
                image = open('cache' + filename, 'rb')
                body = image.read()
                http_req = bytes("HTTP/1.0 200 OK\nContent-Type: image/png\n\n", 'utf-8') + body
                #client_connection.send(http_req)
                image.close()
        if(file_type == 'image/jpeg'):
                fin = open('cache' + filename, 'rb')

        elif(file_type == 'video/mp4'):
                fin = open('cache' + filename, 'rb')
        else:
         # Check if we have this file locally
            html = open('cache' + filename, 'rb')
            print(filename)
            body = html.read()
            #http_req = ("HTTP/1.0 200 OK\nContent-Type: text/html\n\n"+body, 'ascii')
            #client_address.send(http_req)
            html.close()

        print("Read from cache")
        # If we have it, let's send it
        return body
    except IOError:
        return None


def fetch_from_server(filename, serverPath):
    url = 'http://{}'.format(serverPath) + filename
    # print(url)
    q = Request(url)
    try:
        response = urlopen(q)
        # Grab the header and content from the server req
        response_headers = response.info()
        content = response.read()
        return content
    except HTTPError:
        return None


def save_in_cache(filename, content):
    print('Saving a copy of {} in the cache'.format(filename))
    #print('Saving a copy of {} in the cache'.format(filename))
    try:
        os.mkdir("./cache")
    except:
        pass
    my_file=open('cache'+filename, 'wb+')
    my_file.write((content))
    my_file.close()

if __name__ == '__main__':
    main()
