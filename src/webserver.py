'''
Currently, this web server handles only one HTTP request at a time which in
practice is not efficient for handling multiple connections but it gives us a
starting point for looking at the HTTP protocol.
'''

# Import socket module
from socket import *

import sys                                  # In order to terminate the program
import getopt                               # for processsing of args from cmd
import os                                   # file API <-allows you to acess
                                            # the file system
import re                                   # regular expression library
                                            # <- handy for string processing
from datetime import datetime, timedelta    # for managing times - Handy things


def main(argv):

    serverPort = 6789

    # Get the port number at start up, but will default to 6789
    try:
        opts, args = getopt.getopt(argv,"hp:",["port="])
    except getopt.GetoptError:
        print ('webserver.py -p <port number>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('webserver.py -p <port number>')
            sys.exit()
        elif opt in ("-p", "--port"):
            serverPort = int(arg)

    print('Server is running on port ', serverPort)

    # Create a TCP server socket
    # (AF_INET is used for IPv4 protocols)
    # (SOCK_STREAM is used for TCP)
    # This sets up a TCP sockect
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Bind the socket to server address and server port
    serverSocket.bind(("", serverPort))

    # Listen to at most 1 connection at a time
    serverSocket.listen(1)

    # Server should be up and running and listening to the incoming connections
    # keep looping forever
    while True:
        print('The server is ready to receive data....')

        # Set up a new connection from the client
        connectionSocket, addr = serverSocket.accept()

        # If an exception occurs during the execution of try clause
        # the rest of the clause is skipped
        # If the exception type matches the word after except
        # the except clause is executed
        """
        Things to check:
            1. type of request - Is it supported or unsupported
            2. the resource that is being looked for
            3. the path (assuming that the root is in the same directory as the
            server)
            4. check the encoding type
            5. generate a response header with the correct information - You
            will need to think about the structure of what this need to be based
            on the requirements for the lab.
            6. send the response

        TIP:
            -check out what spilt() does to a Python string as you might find
            it useful.

        Remember:
            -The socket connections have been taken care of for you; all you
            need to concentrate on is the L5 protocol for HTTP.
        """
        try:
            # Receives the request message from the clientself.
            # It will wait until data has been recieved from client
            # The decode(encoding='UTF-8') ensurse that the data is interpreted
            # as ASCII
            message = connectionSocket.recv(1024).decode(encoding='UTF-8')
            # print the HTTP request type of message - for diagnoistics
            print(message)  # this should print out what was received from the
                            # client

            responseHeader = ""       # this is your empty response
            #-------------------------------------------------------------------START CODING HERE! -------------------------------------------#
            # Start your coding here!!
            def http_date():
                #Grabbing the date and time now
                now = datetime.now()
                #print(now.strftime("%a, %d %b %Y %H:%M:%S GMT"))
                #"DOW", DD, "MTH", YYYY, HH:MM:SS GMT
                return now.strftime("%a, %d %b %Y %H:%M:%S GMT")
            
            def norm_path(path):
                #according to assignment details, / means standard index.html page
                if path.endswith("/"):
                    path += "index.html"
                elif "." not in os.path.basename(path):
                    path += ".html"
                return "." + path; 
            
            def build_response(status, content_type, body=b""):
                #The RFC 7230 defines the HTTP/1.1 message syntax 
                """
                <status-line>               -->HTTP-version SP status-code SP reason-phrase CRLF
                <field-name>: <field-value> -->Data about the response
                <field-name>: <field-value> -->seperate headers by a CRLF
                ...
                <CRLF>                      
                [message-body]               -->optional (error page)
                """
                #SP = space, CRLF = Carriage Return Line Feed
                #status-line = HTTP-version SP status-code SP reason-phrase CRLF
                #Also ensuring body is bytes
                if isinstance(body, bytes):
                    body_bytes = body
                headers = (
                    f"HTTP/1.1 {status}\r\n"
                    f"Date: {http_date()}\r\n"
                    "Server: MyMostAmazingServerInTheWholeWideWorld/0.1\r\n"
                    f"Content-Length: {len(body_bytes)}\r\n"
                    f"Content-Type: {content_type}\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                ).encode("UTF-8")
                return headers + body_bytes
            def get_content_type(localpath):
                    end = re.search(r'\.([^./\\]+)$', localpath)
                    if end:
                        end = '.' + end.group(1)
                    #print(end)
                    if end == ".html" or end == ".htm":
                        return "text/html"
                    if end == ".gif":
                        return "image/gif"
                    if end == ".jpg":
                        return "image/jpeg"
                    if end == ".png":
                        return "image/png"
                    if end == ".css":
                        return "text/css"
                    if end == ".js":
                        return "application/javascript"
                    if end == ".pdf":
                        return "application/pdf"
                    if end == ".json":
                        return "application/json"
                    if end == ".ico":
                        return "image/x-icon"
                    #Not supported
                    return None
            # This line forces the application to through a IO exception
            # You will want to remove it, once you have tested your application
            #raise IOError

            # Things to do...
            # Extract the path of the requested object from the message
            # You will need to extract out the request method and the path
            # The first part of the HTTP header is the request method
            # The path is the second part of HTTP header - You will need to do
            # further processing on the path to check the criteria of what is
            # permitted, etc
            # IMPORTANT:  Start with the most basic request for index.html

            """Things to do (pseudocode): edition
            1) Grab the request type and the path
            2) Check if the request type is a GET
                If it is not a GET, return error
            3) Check the path
                If it is a /, then you will need to return the index.html file
                If it is something else, you will need to check that it is valid
                    If it is valid, then you will need to check that the file exits
                        If it does not exist, then return a 404 Not Found error
            4) If the file exists, then you will need to create the response header
                need to check the type of file being requested so you can set the correct encoding type
            5) Send the response header back to the client
            6) Send the content of the requested file to the connection socket
            """
            
            # --- Grabbing the request type and path from the message
            split_message = message.split()
            if len(split_message) < 2:
                #Somethindg wrong with the request
                print("len split message caused an IO ERRORRRRRRR")
                raise IOError
            request_type = split_message[0]
            path = split_message[1]
            
            
            # --- Check if the request type is a GET
            
            if request_type != "GET":
                responseHeader = build_response(
                    "405 Method Not Allowed",
                    "text/html", 
                    "<html><head></head><body><h1>405 Method Not Allowed</h1></body></html>"
                )
                #connectionSocket.send(responseHeader.encode(encoding = 'UTF-8')) 
                connectionSocket.send(responseHeader) 
                connectionSocket.close()
                continue
                #raise IOError
            

            # --- Normalize the path 
            localpath = norm_path(path)
            """ TESTING because I was pulling my hair out 
            print(f"Request type: {request_type}------------------------------------------------------------")
            print(f"Raw path: {path}")
            print(f"Normalized path: {localpath}")
            print(f"File exists? {os.path.isfile(localpath)}")
            """
            # --- Check if the path is valid
            if ".." in localpath:
                responseHeader = build_response(
                    "403 Forbidden",
                    "text/html", 
                    "<html><head></head><body><h1>403 Forbidden</h1></body></html>"
                )
                #connectionSocket.send(responseHeader.encode(encoding = 'UTF-8')) 
                connectionSocket.send(responseHeader) 
                connectionSocket.close()
                continue
                #raise IOError
            
            # --- Check if the file exists
            if not os.path.isfile(localpath):
                responseHeader = build_response(
                    "404 Not Found", 
                    "text/html",
                    "<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n"
                    )
                #connectionSocket.send(responseHeader.encode(encoding = 'UTF-8')) 
                connectionSocket.send(responseHeader) 
                connectionSocket.close()
                continue
                #raise IOError
            # --- checking file extension 
            file_extension = get_content_type(localpath)
            if file_extension is None:
                responseHeader = build_response(
                    "415 Unsupported Media Type",
                    "text/html",
                    "<html><head></head><body><h1>415 Unsupported Media Type</h1></body></html>\r\n"
                )
                #connectionSocket.send(responseHeader.encode(encoding = 'UTF-8'))
                connectionSocket.send(responseHeader) 
                connectionSocket.close()
                continue
                #raise IOError
            
            #Read/respond with file
            with open(localpath, "rb")  as f:
                body = f.read()
            
            responseHeader = build_response(
                "200 OK",
                file_extension,
                body
            )
            #connectionSocket.send(responseHeader.encode(encoding='UTF-8'))
            #Test usage
            #print(responseHeader)
            connectionSocket.send(responseHeader)
            # if this is a binary file (ie png, jpg, pdf) is must be encoded for
            # proper transfer and you need to think about the length....

            #once everything is done, send the response header back
            #connectionSocket.send(responseHeader.encode(encoding='UTF-8'))

            # Send the content of the requested file to the connection socket

            #send something else to indicate the end of the response header

            # Close the client connection socket
            connectionSocket.close()

        except IOError:
                # Send HTTP response message for file not found
                # this will always need to be run, if a file can't be Found
                # assuming it is a valid type
                connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode(encoding='UTF-8'))
                connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode(encoding='UTF-8'))
                # Close the client connection socket
                connectionSocket.close()


    serverSocket.close()
    # Terminate the program after sending the corresponding data
    sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])
