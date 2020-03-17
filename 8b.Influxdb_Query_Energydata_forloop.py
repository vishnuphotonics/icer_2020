# This program reads influxdb database and extracts a single value of interest
# The program loops through the influx data-bases, extracts value and sums the energy
# Check the energy database name in the second section
import os,time,datetime,argparse,dateutil.parser,pandas as pd
from influxdb import InfluxDBClient
from pandas import DataFrame, read_csv
from datetime import timedelta, date
import json

invertors=["SN0005000043200013","SN0005000043200033","SN0005000043200034","SN0005000043200044","SN0005000043200048",\
"SN0005000043200066","SN0005000043200083","SN0005000043200089"] # "SN0005000043200005",SN0005000043200028",,"SN000500004320007B"
# Extract data from influxdb
sumenergy=0
for i in invertors:
    print (i)
    invertorID=i
    dbClient = InfluxDBClient('localhost', 8086, 'root', 'root', invertorID)
    loginRecords = dbClient.query('select Eac_Total from SN0005000043200013 order by desc limit 1') # lists last value
    for p in loginRecords.get_points():
        i=p
    #    print (p)
    person_dict = json.dumps(p)
    q=json.loads(person_dict)
    q.values()
    #print (q.values())
    yyy=list (q.values()) ; 
    Energy=(yyy[1]) ; print ("Energy =",Energy)
    sumenergy=sumenergy+Energy
print (sumenergy)

#*******************************************#
# upload to influxdb cloud database
host='localhost'
port=8086
user = 'root'
password = 'root'
dbname = 'energy' # energy database name 

# Temporarily avoid line protocol time conversion issues #412, #426, #431.
protocol = 'json'
client = InfluxDBClient(host, port, user, password, dbname)
client.create_database(dbname)
json_body= [{ "measurement":"sumenergy",
#"tags":{"Energy": "Energy"},
#"time":Timeadjusted[i],
"fields":{"Energy":sumenergy}}]
client.write_points(json_body)




