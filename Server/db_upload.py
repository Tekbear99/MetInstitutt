import pymysql

# Open database connection
db = pymysql.connect("193.93.253.25","codespo","45Pvilfd","codespo_metinstitutt")

# prepare a cursor object using cursor() method
cursor = db.cursor()

timestamp = "Hei"
ohm = 101.27
R = 2.3


# Prepare SQL query to INSERT a record into the database.
sql = "INSERT INTO data_main_min(TIMESTAMP, OHM, CELSIUS, UPTIME, DOWNTIME) \
         VALUES ('%s', '%f', '%f', '%i', '%i' )" % \
         (timestamp, ohm, R, 1, 0)
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()

# disconnect from server
db.close()
