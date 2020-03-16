import os,time,datetime,argparse,dateutil.parser,pandas as pd
from influxdb import InfluxDBClient
from pandas import DataFrame, read_csv
from datetime import timedelta, date

#invertors=["SN0005000043200005","SN0005000043200013","SN0005000043200028","SN0005000043200033","SN0005000043200034","SN0005000043200044","SN0005000043200048",\
#"SN0005000043200083","SN0005000043200089","SN000500004320007B"]

invertorID="SN0005000043200013"
dbClient = InfluxDBClient('localhost', 8086, 'root', 'root', invertorID)

# Query the IPs from logins have been made

#loginRecords = dbClient.query('select * from /./;') # lists all values

loginRecords = dbClient.query('select * from /./ limit 2;') # lists only two values

loginRecords = dbClient.query('select * from /./ order by ASC limit 1;') # lists last value

 
 # Print the time series query results

print(loginRecords)

loginRecords = dbClient.query('select Eac_Total from SN0005000043200013 order by asc limit 1') # lists last value
print(loginRecords)

loginRecords = dbClient.query('select Eac_Total from SN0005000043200013 order by asc limit 1') # lists last value
print(loginRecords)

g= loginRecords ; print (g)    # Lists value

t=list(g) ;print (t); print (type(t))
print (t[0])

rs =dbClient.query("SELECT * from SN0005000043200013 order by asc limit 1") 
print (rs)

for p in loginRecords.get_points():
    print (p)

import json
person_dict = json.dumps(p)
print( person_dict)
print (len(person_dict))
#print(person_dict["Eac_Total"])
q=json.loads(person_dict)
print (type(q))
q.values()
print (q.values())
yyy=list (q.values()) ; print (yyy[1])