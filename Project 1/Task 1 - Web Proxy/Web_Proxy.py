from socket import *
import sys
import os

#http://127.0.0.1:1000/www.neverssl.com     for testing

# Create a server socket, bind it to a port and start listening
# Fill in start.
port = 1000
host = '127.0.0.1'
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind((host, port))
tcpSerSock.listen(1)
# Fill in end.
while 1:
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(4096)
    print(message)

    # Extract the filename from the given message
    filename = message.split()[1].partition("/".encode())[2]
    print(filename)
    fileExist = "false"
    filetouse = os.path.join(sys.path[0], filename.decode())#"/" + filename
    print(filetouse)

    try:
        # Check whether the file exist in the cache
        f = open(filetouse[1:], "r")
        outputdata = f.readlines()
        fileExist = "true"
        print('File Exists') # remove after testing

        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode())
        tcpCliSock.send("Content-Type:text/html\r\n".encode())
        # Fill in start.
        created_response = ""

        #for every element in output data, add it to the response
        for element in outputdata:
            created_response += element
        
        # Fill in end.
        tcpCliSock.send(created_response.encode())
        print('Read from cache')

    # Error handling for file not found in cache
    except IOError:

        if fileExist == "false":
            # Create a socket on the proxy server
            # Terrible naming convention but its the template soooo?
            c = socket(AF_INET, SOCK_STREAM)
            hostn = (filename.replace("www.".encode(), "".encode(), 1)).decode()
            #print(hostn) for testing

            try:
                # Connect to the socket to port 80
                # Fill in start.
                c.connect((hostn, 80))
                # Fill in end.
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                #fileobj = c.makefile('r', 0)
                #fileobj.write(("GET "+"http://" + filename.decode() + "HTTP/1.0\n\n").encode())
                created_request = ("GET "+"http://" + filename.decode() + "HTTP/1.0\n\n").encode()
                c.send(created_request)
                temp_response = c.recv(4096)
                created_response = ""

                while 1:
                    print(str(temp_response))
                    created_response = created_response + str(temp_response)
                    temp_response = c.recv(4096)

                # Read the response into buffer
                # Fill in start.
                #temp_buffer = fileobj.readlines()
                # Fill in end.
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                tmpFile = open("./" + filename,"wb")
                tmpFile.write(created_response)
                tmpFile.close()

                tcpSerSock.send(created_response)
                print("read from cache")
                # Fill in start.
                #length = len(temp_buffer)

                #for item in range(0, length):
                 #   tmpFile.write(temp_buffer[item])
                  #  tcpCliSock.send(temp_buffer[item])
                # Fill in end.
            except:
                print("Illegal request")
        else:
        # HTTP response message for file not found
        # Fill in start.
            pass
            #tcpCliSock.send("HTTP/1.1 404 Not Found \r\n\r\n")
        # Fill in end.
# Close the client and the server sockets
tcpCliSock.close()
# Fill in start.
tcpSerSock.close()
# Fill in end.