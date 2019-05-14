import socket
import sys
import time


import RPi.GPIO as GPIO


#switches on the H-bridge
L293E_IN1 = 21  
L293E_IN2 = 26
L293E_IN3 = 16
L293E_IN4 = 20
EN_1 = 13
EN_2 = 12
IR_PIN = 19

def RobotInit():
    GPIO.setmode(GPIO.BCM)
    #initializing GPIO pins to low outputs 
    GPIO.setup(L293E_IN1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(L293E_IN2,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(L293E_IN3,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(L293E_IN4,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(EN_1,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(EN_2,GPIO.OUT,initial=GPIO.HIGH)

#movement logic
def RobotFWD():
	GPIO.output(L293E_IN1,False)
	GPIO.output(L293E_IN2,True)
	GPIO.output(L293E_IN3,False)
	GPIO.output(L293E_IN4,True)
    
def RobotBACK():
	GPIO.output(L293E_IN1,True)
	GPIO.output(L293E_IN2,False)
	GPIO.output(L293E_IN3,True)
	GPIO.output(L293E_IN4,False)

def RobotLEFT():
	GPIO.output(L293E_IN1,False)
	GPIO.output(L293E_IN2,True)
	GPIO.output(L293E_IN3,True)
	GPIO.output(L293E_IN4,False)

def RobotRIGHT():
	GPIO.output(L293E_IN1,True)
	GPIO.output(L293E_IN2,False)
	GPIO.output(L293E_IN3,False)
	GPIO.output(L293E_IN4,True)
	
def RobotSTOP():
	GPIO.output(L293E_IN1,False)
	GPIO.output(L293E_IN2,False)
	GPIO.output(L293E_IN3,False)
	GPIO.output(L293E_IN4,False)

def RobotDeInit():
    GPIO.cleanup()


RobotInit()
GPIO.setup(IR_PIN,GPIO.IN,pull_up_down=GPIO.PUD_UP)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.settimeout(0.0025)
sock.setblocking(0)

server_address = ('localhost', 10000)#192.168.56.1
print(server_address)

print('starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    try:
        # Wait for a connection
        print >>sys.stderr, 'waiting for a connection'
        connection, client_address = sock.accept()
        connection.settimeout(0.0025)
        print >>sys.stderr, 'connection from', client_address
        break;
    except socket.timeout:
        pass
    except socket.error:
        #exit from here
        pass


# Receive the data in small chunks and retransmit it
while True:
    iRStatus = GPIO.input(IR_PIN)
    #print(iRStatus)
    if(iRStatus == 1):
        RobotSTOP()
    try:
        data = connection.recv(16)
        if data != '':
            print >>sys.stderr, 'received "%s"' % data
            if data[0] == 'w':
                RobotFWD()
            elif data[0] == 'a':
                RobotLEFT()
            elif data[0] == 's':
                RobotSTOP()
            elif data[0] == 'd':
                RobotRIGHT()
            elif data[0] == 'b':
                RobotBACK()
        time.sleep(0.01)
    except socket.timeout:
        #print('timeout')
        pass
    except socket.error:
        connection.close()
        sock.close()
        RobotDeInit()
        break
    except KeyboardInterrupt:
        # Clean up the connection
        connection.close()
        sock.close()
        RobotDeInit()
        break;