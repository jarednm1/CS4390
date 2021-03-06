from socket import *
import sys

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerPort = 8899
tcpSerSock.bind(('', tcpSerPort))
tcpSerSock.listen(5)
while 1:
    print("Ready to serve ...")
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(4096).decode()
    print("Message: ",message)
    print("Message: split: ",message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print("Filename: ",filename)
    fileExist="false"
    try:
        tcpCliSock.send(("HTTP/1.0 200 OK\r\n").encode())
        tcpCliSock.send(("Content-Type:text/html\r\n").encode())
        with open(filename,"r") as f:
            outputdata = f.readlines()
        join_er = "".join(outputdata)
        tcpCliSock.send(join_er.encode())
        fileExist = "true"
        print("Read from cache")

    except IOError:
        if fileExist=="false":
            c = socket(AF_INET,SOCK_STREAM) 
            hostn = filename.replace("www.","",1)
            try:
                c.connect((hostn,80))
                request = "GET / HTTP/1.1\r\nHost: %s\r\n\r\n" % hostn
                c.sendall(request.encode())
                fileobj = c.recv(10000)
                tcpCliSock.send(fileobj)
                cache_file = open(filename, "w")
                while (len(fileobj)>0):
                    fileobj = c.recv(10000)
                    tcpCliSock.send(fileobj)
                    cache_file.write(fileobj)
                cache_file.close()
            except:
                print("Illegal request")
        else:
            tcpCliSock.send(("HTTP/1.0 404 Not Found\r\n").encode())
            tcpCliSock.send(("Content-Type:text/html\r\n").encode())
    tcpCliSock.close()

tcpSerSock.close()
#C:\Users\Syed\OneDrive - Bowling Green State University\Notebooks\Academics\Sem6\CS4390\Assignments\Project\Project 1\CS4390\Project 1\Task 1 - Web Proxy
#http://localhost:8899/www.neverssl.com
