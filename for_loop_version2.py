# This program creates the df for the specified not of dates
import os,time,datetime,argparse,dateutil.parser,pandas as pd
from influxdb import DataFrameClient
from influxdb import InfluxDBClient
from pandas import DataFrame, read_csv
from datetime import timedelta, date



##### Program starts #####
invertorID="SN0005000043200013"
os.chdir("/home/vishnu/Documents/icer/"+invertorID)

      
#( date,month,year); GENERATE DATES .CSV FORMAT
start = datetime.datetime.strptime("01-01-2018", "%d-%m-%Y")
end = datetime.datetime.strptime("20-1-2018", "%d-%m-%Y")   # One day after the end date
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
g=[]
for date in date_generated:
    start_date=(date.strftime("%d"))
    end_date=(date.strftime("%d"))
    month=(date.strftime("%m"))
    year=(date.strftime("%Y"))
    filename=(str(year)+str(month)+str(start_date))+".csv"
    #print (filename)
    g.append(filename)
#    print (g)
print (g)
print ("no of days=",len(g))

df=pd.DataFrame()
for x in range(0, len(g)):
    dg=pd.read_csv(g[x])
    df=df.append(dg,ignore_index=True)
    print ("fileno="+str(x),"filename="+str(g[x]+'.csv') )
print (df)
print(df)
    
