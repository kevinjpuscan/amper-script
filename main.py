
import os
import psycopg2
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

dbHost=os.getenv('DB_HOST')
dbName=os.getenv('DB_NAME')
dbPort=os.getenv('DB_PORT')
dbUser=os.getenv('DB_USER')
dbPass=os.getenv('DB_PASS')


def getDataSensor():
    return 10.1

def saveValue(value):
    conn = psycopg2.connect(database=dbName,user=dbUser,password=dbPass, host=dbHost)
    cur = conn.cursor()
 
    cur.execute("select add_electric("+str(value)+"::real,'"+str(datetime.now())+"'::timestamp);")
    conn.commit()

    if(conn):
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")
            

if __name__ == '__main__':
    watt = getDataSensor()
    saveValue(watt)
    