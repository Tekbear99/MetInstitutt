import socket
import sys
import time
import math
import sched

#Constants#
R_0 = 100
a = 3.9083 * (10**(-3))
b = -5.775 * (10**(-7))

updateTimer = sched.scheduler(time.time, time.sleep)

def space():
    print()
    print()

def main(timer):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    ip = "37.26.220.85"
    port = 4002

    print("Connecting...")
    sock.connect((ip, port))
    print("Connected to", ip, "with port", port)

    try:

        # Send data
        message = "#04" + str(chr(13))
        print('Sending "%s"' % message)
        sock.send(message.encode('utf-8'))

        # Look for the response
        amount_received = 0
        amount_expected = 9

        dChar = []
        while amount_received < amount_expected:
            data = sock.recv(1)
            amount_received += len(data)
            dataFull = str(data,'utf-8')

            dVal = dataFull
            dChar.append(dVal)

        dataRes = float(dChar[2] + dChar[3] + dChar[4] + dChar[5] + dChar[6] + dChar[7])
        print(dataRes)


        R = float(dataRes)
        t = ((((-R_0)*a) + math.sqrt((R_0 ** 2) * (a ** 2) - 4 * R_0 * b * (R_0 - R))) / (2 * R_0 * b))
        if(t == -0.0):
            print(int(0.0))
        else:
            currentTemp = ("%.2f" % t)
            print("Exact temp:", t)
            print(currentTemp)


    finally:
        print('Closing Socket...')
        sock.close()
        print('Socket closed!')
        updateTimer.enter(5, 1, main, (timer,))

updateTimer.enter(5, 1, main, (timer,))
updateTimer.run()
