# Importing modules
import socket
import sys
import pymysql
import time
import math
import datetime
import os
import threading as thr

# Setting an array the holds 12 temperatures per minute
MinuteMeasurements = []

# Constants
R_0 = 100
a = 3.9083 * (10 ** (-3))
b = -5.775 * (10 ** (-7))

# Creating a socket to later connect to a server
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Defining the IP and port we wish to connect to
ip = '37.26.220.85'
port = 4002

# Connect to the database
db = pymysql.connect('193.93.253.25','codespo','45Pvilfd','codespo_metinstitutt')

# Prepare a cursor object using cursor() method for the database
cursor = db.cursor()

# Restarting the program from line 1
def systemReboot():
    python = sys.executable
    os.execl(python, python, * sys.argv)

# Defining a mainfunction for the script
def mainframe():

    # Making sure that WinError#10056 does not occur
    try:

        # Setting a timer to run function every 5 seconds
        thr.Timer(5.0, main).start()

        # Setting a timer to reboot script every hour
        thr.Timer(3600.0, systemReboot).start()

        try:

            # Sending data to server
            packet = '#04' + str(chr(13))
            socket.send(packet.encode('utf-8'))

            # Setting the limit for amount of incoming information
            amount_received = 0
            amount_expected = 9

            # Splitting characters from received data so only numbers remain
            dChar = []
            while (amount_received < amount_expected):
                data = socket.recv(1)
                amount_received += len(data)
                dataFull = str(data,'utf-8')

                dVal = dataFull
                dChar.append(dVal)

            # Collecting specific integers from received data
            dataResults = foat(dChar[2] + dChar[3] + dChar[4] + dChar[5] + dChar[6] + dChar[7])


            R = float(dataResults)
            t = ((((- R_0) * a) + math.sqrt((R_0 ** 2) * (a ** 2) - 4 * R_0 * b * (R_0 - R))) / (2 * R_0 * b))
            if(t == -0.0):

                # Debugging given value for temperatur when provided ohm is 100.00
                currentTemp = 0.0
            else:

                # Rounding off to a two decimal value
                currentTemp = ('%.2f' % t)

            # Sending all measurements to array
            MinuteMeasurements.append(float(currentTemp))

            # Cheching if length of array is 12 or more
            if(len(MinuteMeasurements) >= 12):

                # Setting timestamp to average temperature per minute
                timestamp = '{:%d.%m.%Y  %H:%M:%S}'.format(datetime.datetime.now())

                # Finding average temperature per minute
                avrgMeasurement = sum(MinuteMeasurements) / len(MinuteMeasurements)

                # Rounding off average temperature to two decimals
                avrgTemp = float('%.2f' % avrgMeasurement)

                # Prepare SQL query to INSERT a record into the database
                sql = 'INSERT INTO data_main-min(TIMESTAMP, OHM, CELSIUS, UPTIME, DOWNTIME) VALUES ('%s', '%f', '%f', '%i', '%i')' % (timestamp, R, avrgTemp, 1, 0)

                try:

                    # Execute the SQL command
                    cursor.execute(sql)

                    # Commit your changes in the database
                    db.commit()

                    print('Data transfer successfull')

                except:

                    # Rollback in case there is any error
                    db.rollback()

                    print('Data transfer failed')

                # Print result to console
                print(timestamp + '  ' + str(avrgTemp))

                # Clearing array for measurements for next minute
                MinuteMeasurements.clear()

            else:

                # If array is not longer than or equal to 12: ignore this if/else statement
                pass

            # Wait 5 seconds before restarting function
            time.sleep(5)

        # In case of error while sending or receiving data, try closing socket and reboot
    except:

        # Closing the socket
        socket.close()

        try:

            # Trying to restart the main function without shutting down
            mainframe()

        except:

            # Rebooting program when program fails
            systemReboot()

    except OSError:

        # Rebooting program if receiving message about WinError
        systemReboot()





#------------------------Start of program------------------------#

print('Connection...')

# Making sure that the connection is made before sending data
try:

    # Connecting to the server via socket
    socket.connect((ip, port))

    # Setting the time of connection to the server if successfull
    connectionTime = '{:%H:%M:%S}'.format(datetime.datetime.now())

    print('Connected to 37.26.220.85  with port 4002 @', connectionTime)
    print('---------------------------------------------------')
    mainframe()

# In case of Connection Error, reboot program
except ConnectionRefusedError:
    print()
    print()
    print('Connection failed')
    print('Could not connect to IP: ' + '37.26.220.85 ' + ' port: ' + str(port))

    # Waiting 15 seconds before trying to reboot program
    time.sleep(15)

    # Rebooting program if connection to server fails
    systemReboot()
