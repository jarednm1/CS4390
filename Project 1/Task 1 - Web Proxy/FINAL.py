from socket import *
import sys

#if len(sys.argv)<=1:
#	print('Usage : " python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
#	sys.exit(2)


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
    try:
        tcpCliSock.send(("HTTP/1.0 200 OK\r\n").encode())
#        tcpCliSock.send(("Content-Type:text/html\r\n").encode())
        c = socket(AF_INET,SOCK_STREAM) 
        #hostn = gethostbyname(filename)
        hostn = filename.replace("www.","",1)
        #print(hostn)
        try:
            c.connect((hostn,80))
            request = "GET / HTTP/1.1\r\nHost: %s\r\n\r\n" % hostn
            c.sendall(request.encode())
            fileobj = c.recv(10000)
            tcpCliSock.send(fileobj)
            #print("THIS IS THE FILE: ",fileobj.decode())
            while (len(fileobj)>0):
                fileobj = c.recv(10000)
                tcpCliSock.send(fileobj)
            #tmpFile = open("./" + filename, "wb")
            #for i in range(0, len(fileobj)):
            #    tmpFile.write(fileobj[i])
            #    tcpCliSock.send(fileobj[i])
            #tcpCliSock.send("\r\n".encode())
        except:
            print("Illegal request")
    except IOError:
        tcpCliSock.send(("HTTP/1.0 404 Not Found\r\n").encode())
        tcpCliSock.send(("Content-Type:text/html\r\n").encode())
    tcpCliSock.close()

# Fill in start.
tcpSerSock.close()
# Fill in end.
#C:\Users\Syed\OneDrive - Bowling Green State University\Notebooks\Academics\Sem6\CS4390\Assignments\Project\Project 1\CS4390\Project 1\Task 1 - Web Proxy
#http://localhost:8899/www.neverssl.com
