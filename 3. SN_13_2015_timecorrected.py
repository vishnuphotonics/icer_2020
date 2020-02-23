# This program creates the df for the specified no of dates : Time 5 hours 30 minutes
import os,time,datetime,argparse,dateutil.parser,pandas as pd
from influxdb import DataFrameClient
from influxdb import InfluxDBClient
from pandas import DataFrame, read_csv
from datetime import timedelta, date

##### Program starts #####
invertorID="SN0005000043200013"
os.chdir("/home/vishnu/darfondata/"+invertorID)


#( date,month,year); GENERATE DATES .CSV FORMAT
start = datetime.datetime.strptime("26-08-2015", "%d-%m-%Y")
end = datetime.datetime.strptime("28-08-2015", "%d-%m-%Y")   # One day after the end date
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
g=[]
for date in date_generated:
    start_date=(date.strftime("%d"))
    end_date=(date.strftime("%d"))
    month=(date.strftime("%m"))
    year=(date.strftime("%Y"))
    filename=(str(year)+str(month)+str(start_date))+".csv"
    df=pd.DataFrame()
    dg=pd.read_csv(filename)
    df=df.append(dg,ignore_index=True)
    df.insert(0,'Timeadjusted',0) # df.insert(idx,col_name,value)
    df['Timeadjusted'] = pd.to_datetime(df.Time)-pd.Timedelta(hours=5,minutes=30)
    #Identify and drop NAN Values
    tt=df[df['Timeadjusted'].isnull()]
    print (tt)
    df=df.dropna()
    # prints dropped df
    df=df.reset_index(drop=True)
    print(df)
    newsize=len(df) 
    print ("new df size",newsize)
    print (df.dtypes)
    #print (filename)

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
      # upload to influxdb cloud
    host='localhost'
    port=8086
    user = 'root'
    password = 'root'
    dbname = 'test'
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

    
  print (df)
