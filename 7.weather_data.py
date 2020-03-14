
# import required modules 
# This program creates influxdb database for a given lat -long
import os,time,datetime,argparse,dateutil.parser,pandas as pd
from influxdb import DataFrameClient
from influxdb import InfluxDBClient
from pandas import DataFrame, read_csv
from datetime import timedelta, date
import requests, json 

# Enter your API key here 

api_key = "078cb7f06229836e435d1deda28f61ce"
# base_url variable to store url 
base_url = "http://api.openweathermap.org/data/2.5/weather?"
  
# Give city name 
city_name = "Bangalore,IN"


# complete_url variable to store 
# complete url address 
complete_url = base_url + "appid=" + api_key + "&q=" + city_name 
  
# get method of requests module 
# return response object 
response = requests.get(complete_url) 
  
# json method of response object  
# convert json format data into 
# python format data 
x = response.json() 
print (x) 

# Now x contains list of nested dictionaries 
# Check the value of "cod" key is equal to 
# "404", means city is found otherwise, 
# city is not found 
if x["cod"] != "404": 
  
    # store the value of "main" 
    # key in variable y 
    y = x["main"] 
    g=x["wind"]
    print ("wind=",g)
    current_windspeed = g["speed"]
    # store the value corresponding 
    # to the "temp" key of y 
    current_temperature = y["temp"]-273.15
    # store the value corresponding 
    # to the "pressure" key of y 
    current_pressure = y["pressure"] 
  
    # store the value corresponding 
    # to the "humidity" key of y 
    current_humidity = y["humidity"] 
  
    # store the value of "weather" 
    # key in variable z 
    z = x["weather"] 
  
    # store the value corresponding  
    # to the "description" key at  
    # the 0th index of z 
    weather_description = z[0]["description"] 
  
    # print following values 
    print(" Temperature (in kelvin unit) = " +
                    str(current_temperature) + 
          "\n atmospheric pressure (in hPa unit) = " +
                    str(current_pressure) +
#          "\n humidity (in percentage) = " +
#                    str(current_humidiy) +
          "\n description = " +
                    str(weather_description)) 
  
    print("Temperature  = "+str(current_temperature)+" celcius"+
		"\nHumidity = "+str(current_humidity)+"%"+
		"\nAtmospheric pressure  = " +
                    str(current_pressure) +" hPa"+
                 "\nwind speed  = "+str(current_windspeed)+" m/s" )
#else: 

#    print(" City Not Found ") 

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
"fields":{"latitude":latitude,"longitude":longitude,"value":value,\
            "temperature":current_temperature,"humidity":current_humidity,"Atmospheric pressure":current_pressure,"windspeed":current_windspeed}}]
client.write_points(json_body)