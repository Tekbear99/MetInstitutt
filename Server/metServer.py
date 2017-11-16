# Imports
import socket
import sys
import time
import math
import sched
import datetime
import os
import threading

# Setting an array for holding all measurements for one minute
minuteMeasurements = []

# Constants
R_0 = 100
a = 3.9083 * (10**(-3))
b = -5.775 * (10**(-7))

#----------------Previous time-function----------------#

    #Creating a function to time sending of code #04
    #updateTimer = sched.scheduler(time.time, time.sleep)

#------------------------------------------------------#

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
ip = "37.26.220.85"
port = 4002

# Function for shutting down system if ConnectionError
def systemShutdown():
    sys.exit()

# Restarts the entire script if restarting main function fails
def systemReboot():
    python = sys.executable
    os.execl(python, python, * sys.argv)

# Main function for sending and receiving data
def main():

    # Setting an alternative timer to run code every 5 seconds
    threading.Timer(5.0, main).start()

    try:

        # Send data
        message = "#04" + str(chr(13))
        #print('Sending "%s"' % message)
        sock.send(message.encode('utf-8'))

        # Look for the response
        amount_received = 0
        amount_expected = 9

        # Splitting characters from received data so only numbers remain
        dChar = []
        while amount_received < amount_expected:
            data = sock.recv(1)
            amount_received += len(data)
            dataFull = str(data,'utf-8')

            dVal = dataFull
            dChar.append(dVal)

        # Collecting specific integers from reveived data
        dataRes = float(dChar[2] + dChar[3] + dChar[4] + dChar[5] + dChar[6] + dChar[7])

        # Formula for finding temperature using a measurement of ohm
        R = float(dataRes)
        t = ((((-R_0)*a) + math.sqrt((R_0 ** 2) * (a ** 2) - 4 * R_0 * b * (R_0 - R))) / (2 * R_0 * b))
        if(t == -0.0):

            # Debugging given value for temperatur when provided ohm is 100.00
            currentTemp = 0.0
        else:

            # Rounding off to a two decimal number
            currentTemp = ("%.2f" % t)

        # Sending all measurements to array
        minuteMeasurements.append(float(currentTemp))

        # Checking if length of array is 12 or more
        if(len(minuteMeasurements) >= 12):

            # Adding timestamp to average temperature per minute|
            timestamp = '{:%d.%m.%Y  %H:%M:%S}'.format(datetime.datetime.now())

            # Finding temp average per minute
            avrgMeasurement = sum(minuteMeasurements) / len(minuteMeasurements)

            # Rounding off average temperature to two decimal
            avrgTemp = float("%.2f" % avrgMeasurement)
            print(timestamp + "   " + str(avrgTemp))

            # Clearing array for measurements for next minute
            minuteMeasurements.clear()
        else:

            # If array is not longer than or equal to 12: ignore this is/else statement
            pass

        # updateTimer.enter(5, 1, main, (timer,))
        time.sleep(5)

    # In case of error while sending or receiving data, try closing socket an rebooting
    except:

        # Closing the socket
        sock.close()
        try:

            # Trying to restart the main function without shutting down
            main()
        except:

            # Rebooting program when program fails
            systemReboot()



#--------Start of program--------#
print("Connecting...")

# Making sure that the connection is made before sending data
try:

    # Connecting to the server via socket
    sock.connect((ip, port))

    # Setting the time of connetion to the server if successful
    connectionTime = '{:%H:%M:%S}'.format(datetime.datetime.now())

    print("Connected to", ip, "with port", port, "@", connectionTime)
    print("---------------------------------------------------")
    main()

# In case of Connection Error, shutdown program
except ConnectionRefusedError:
    print()
    print()
    print('Connection failed')
    print('Could not connect to IP: ' + str(ip) + ' port: ' + str(port))

    # Shutting down program if connection to server fails
    systemShutdown()

#----------------Previous time-function----------------#

# Calling the function Main after time: 5 seconds
#updateTimer.enter(5, 1, main, (updateTimer,))
#updateTimer.run()

#------------------------------------------------------#
