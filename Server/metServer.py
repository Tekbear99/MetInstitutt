# Imported modules
import socket
import sys
import pymysql
import time
import math
import datetime
import os
import threading

# Setting an array for holding all 12 measurements for one minute
minuteMeasurements = []

# Constants
R_0 = 100
a = 3.9083 * (10**(-3))
b = -5.775 * (10**(-7))


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
ip = "37.26.220.85"
port = 4002

# Connect to the database
db = pymysql.connect("193.93.253.25","codespo","45Pvilfd","codespo_metinstitutt")

# Prepare a cursor object using cursor() method for the database
cursor = db.cursor()

# Function for shutting down system if ConnectionError
def systemShutdown():
    sys.exit()

# Restarts the entire script if restarting main function fails
def systemReboot():
    python = sys.executable
    os.execl(python, python, * sys.argv)

# Main function for sending and receiving data
def main():

    #Try to run main function
#    try:

        # Setting a timer to run function every 5 seconds
        threading.Timer(5.0, main).start()

        # Setting timer to force script reboot every 2 hours to prevent WinError 10060
        threading.Timer(3600.0, systemReboot).start()

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

                # Prepare SQL query to INSERT a record into the database.
                sql = "INSERT INTO data_main_min(TIMESTAMP, OHM, CELSIUS, UPTIME, DOWNTIME) \
                         VALUES ('%s', '%f', '%f', '%i', '%i')" % \
                         (timestamp, R, avrgTemp, 1, 0)
                try:
                   # Execute the SQL command
                   cursor.execute(sql)
                   # Commit your changes in the database
                   db.commit()
                   print("Data is sent to database")
                except:
                   # Rollback in case there is any error
                   db.rollback()
                   print("Database Error: Not sending data to database")

                # Print result to console
                print(timestamp + "   " + str(avrgTemp))

                # Clearing array for measurements for next minute
                minuteMeasurements.clear()
            else:

                # If array is not longer than or equal to 12: ignore this is/else statement
                pass

            # Wait 5 seconds before restarting function
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

#    except OSError:

        # Rebooting program if WinError
    #    systemReboot()


#------------------------Start of program------------------------#
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
    systemReboot()
