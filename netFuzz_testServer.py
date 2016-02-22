import socket

sock = socket.socket()
sock.bind( ("", 8080) )
sock.listen(5)

try:
    while 1:
        conn, addr = sock.accept()
        print("New connection from " + addr[0])

        tmp = conn.recv(1024*1024)
        print tmp
        conn.send("AAAAAA".encode('hex'))

        tmp2 = conn.recv(1024*1024)
        print tmp2
        conn.send("BBBBBB".encode('hex'))

        tmp3 = conn.recv(1024*1024)
        print tmp3
        conn.send("CCCCCC".encode('hex'))

        tmp4 = conn.recv(1024*1024)
        print tmp4
        conn.send("DDDDDD".encode('hex'))

        conn.close()
finally: sock.close()
