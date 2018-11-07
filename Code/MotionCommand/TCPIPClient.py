import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

while True:
    try:
        command = raw_input("Enter Command\n")
        print >>sys.stderr, 'sending "%s"' % command
        sock.sendall(command)
    except KeyboardInterrupt:
        break

print >>sys.stderr, 'closing socket'
sock.close()
