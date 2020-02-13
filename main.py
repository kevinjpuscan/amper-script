
import os
import psycopg2
import serial,time
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

dbHost=os.getenv('DB_HOST')
dbName=os.getenv('DB_NAME')
dbPort=os.getenv('DB_PORT')
dbUser=os.getenv('DB_USER')
dbPass=os.getenv('DB_PASS')

serialPort=os.getenv('SERIAL_PORT')



def getDataSensor():
    arduinoPort = serial.Serial(serialPort, 9600, timeout=1)
    time.sleep(2)

    #print('get discart value')
    arduinoPort.write('b'.encode())
    valueInput = arduinoPort.readline().decode()

    for i in range(6):
        arduinoPort.write('b'.encode())
        valueInput = arduinoPort.readline().decode()
        saveValue(valueInput)
        if(i!=5):
            time.sleep(10)

    arduinoPort.close()
    return valueInput

def saveValue(value):
    conn = psycopg2.connect(database=dbName,user=dbUser,password=dbPass, host=dbHost)
    cur = conn.cursor()
 
    cur.execute("select add_electric("+str(value)+"::real,'"+str(datetime.now())+"'::timestamp);")
    conn.commit()

    if(conn):
            cur.close()
            conn.close()
            #print("PostgreSQL connection is closed")
            

if __name__ == '__main__':
    getDataSensor()

    