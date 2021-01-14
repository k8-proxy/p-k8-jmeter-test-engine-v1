# importing the requests library
import requests

# defining the api-endpoint
API_ENDPOINT = "http://localhost:3000/api/datasources"
username="admin"
password="admin@123"

# create influxdb datasource
influx_data = {
  "name":"InfluxDB",
  "type":"influxdb",
  "url":"http://influxdb-service.common",
  "access":"proxy",
  "database":"jmeter",
  "basicAuth": "false"
    }

headers={'content-type': 'application/json'}

try:
  # sending post request and saving response as response object
  r = requests.post(url=API_ENDPOINT, data=influx_data,auth=(username, password))

  # extracting response text

  print("InfluxDB  datasource :%s" % r.text)
except Exception as e:
  print(e)

# create icapserver datasource
icap_data = {
  "name":"icapserver",
  "type":"influxdb",
  "url":"http://influxdb-service.common",
  "access":"proxy",
  "database":"icapserver",
  "basicAuth": "false"
    }

headers={'content-type': 'application/json'}

try:
  # sending post request and saving response as response object
  r = requests.post(url=API_ENDPOINT, data=icap_data,auth=(username, password))

  print("ICAPServer  datasource :%s" % r.text)
except Exception as e:
  print(e)

# create Loki datasource
loki_data = {
  "name":"Loki",
  "type":"loki",
  "url":"http://loki.common:3100",
  "access":"proxy",
  "basicAuth": "false",
  "jsonData":{
    "maxLines": "5000"
   }
}

headers={'content-type': 'application/json'}

try:
  # sending post request and saving response as response object
  r = requests.post(url=API_ENDPOINT, data=loki_data,auth=(username, password))

  print("Loki datasource :%s" % r.text)
except Exception as e:
  print(e)
