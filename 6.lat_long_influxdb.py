# This program creates influxdb database for a given lat -long
import os,time,datetime,argparse,dateutil.parser,pandas as pd
from influxdb import DataFrameClient
from influxdb import InfluxDBClient
from pandas import DataFrame, read_csv
from datetime import timedelta, date

# Lat-long_information
latitude="13.0155"
longitude="77.5681"
value=10

database = "Information"

# upload to influxdb cloud
host='localhost'
port=8086
user = 'root'
password = 'root'
dbname = database
# Temporarily avoid line protocol time conversion issues #412, #426, #431.
protocol = 'json'
client = InfluxDBClient(host, port, user, password, dbname)
client.create_database(dbname)

#print ('currentfile=',newsize)
json_body= [{ "measurement":database,
"tags":{"col3": "col3"},
#"time":Timeadjusted[i],
"fields":{"latitude":latitude,"longitude":longitude,"value":value}}]
client.write_points(json_body)


