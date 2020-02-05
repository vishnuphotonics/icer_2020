# this is a master file - working version for ONE MONTH ONLY
import os,time,datetime,argparse,dateutil.parser,pandas as pd
from influxdb import DataFrameClient
from influxdb import InfluxDBClient
from pandas import DataFrame, read_csv
from datetime import timedelta, date


##### Program starts #####
invertorID="SN0005000043200013"
os.chdir("/home/vishnu/Documents/icer/"+invertorID)
#####functions#####
def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)


#print int(quarter1[0]+","+quarter1[1]+","+quarter1[2])
start_dt = date(2018,1,1)
end_dt = date(2018,1,31)
g=[dt.strftime("%Y%m%d")for dt in daterange(start_dt, end_dt) ] # prints all dates- print g
print (g)
print ('days ='+str(len(g)))
print ("end of file")

df=pd.DataFrame()
for x in range(0, len(g)):
    dg=pd.read_csv(str(g[x])+'.csv')
    df=df.append(dg,ignore_index=True)
    print ("fileno="+str(x),"filename="+str(g[x]+'.csv') )
print (df)
size=len(df) 
print ('old df size=',size)
# insert time adjusted column 
df.insert(0,'Timeadjusted',0) # df.insert(idx,col_name,value)
df['Timeadjusted'] = pd.to_datetime(df.Time)-pd.Timedelta(hours=8,minutes=30)

#Identify and drop NAN Values
tt=df[df['Timeadjusted'].isnull()]
print (tt)
df=df.dropna()
# prints dropped df
print(df)
newsize=len(df) 
print ("new df size",size)
print (df.dtypes)

# preparation for influxdb database
# columns for database
Timeadjusted=pd.to_datetime(df['Timeadjusted'].astype(int))[:]
tempcolumn=df['Temperature']
EACcolumn=df['Eac_Today']
VPVcolumn=df['Vpv']
IACcolumn=df['Iac']
VACcolumn=df['Vac']
PACcolumn=df['Pac']
FACcolumn=df['Fac']
EAC_TOTAL=df['Eac_Total']
IPVcolumn=df['Ipv']
PPVcolumn=df['Ppv']
print ("analyzed time values = \n",Timeadjusted)  # prints converted time column values
print (df)

# upload to influxdb cloud
host='localhost'
port=8086
user = 'root'
password = 'root'
dbname = invertorID
# Temporarily avoid line protocol time conversion issues #412, #426, #431.
protocol = 'json'
client = InfluxDBClient(host, port, user, password, dbname)
client.create_database(dbname)

for i in range(newsize):
    #print ('currentfile=',newsize)
    json_body= [{ "measurement":invertorID,
    "tags":{"col3": "col3"},
    "time":Timeadjusted[i],
    "fields":{"temperature":tempcolumn[i],
                "Eac_today":EACcolumn[i],
                "Vpv":VPVcolumn[i],
                "Iac":IACcolumn[i],
                "Vac":VACcolumn[i],
                "Pac":PACcolumn[i],
                "Fac":FACcolumn[i],
                "Eac_Total":EAC_TOTAL[i],
                "Ipv":IPVcolumn[i],
                "Ppv":PPVcolumn[i]}}]
    client.write_points(json_body)
