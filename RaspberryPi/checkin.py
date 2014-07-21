import discover
import urllib2 
import json

url = "http://10.9.217.133:8080/checkin"

def postData(data):
    jdata = json.dumps({"macAddress":'"'+str(data[0])+'"'})
    urllib2.urlopen(url, jdata)

result = discover.discoverBluetoothDevices()

if len(result) > 1:
    postData(result[0])
