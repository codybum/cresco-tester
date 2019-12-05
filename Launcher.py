
import Utils

#global_controller_id = Utils.startGlobal()
#print(Utils.getContainterIP(global_controller_id))
#Utils.stopContainter(global_controller_id)
#Utils.startAgent("127.0.0.1")



import http.client, urllib.parse
import requests

data = open('/Users/cody/IdeaProjects/agent/mysql-connector-java-8.0.13.jar', 'rb').read()
res = requests.post(url='http://localhost:8181//dashboard/plugins/uploadplugin',
                    data=data,
                    headers={'Content-Type': 'application/java-archive',"X-Auth-API-Service-Key":"BDB"})

# let's check if what we sent is what we intended to send...
import json
import base64

assert base64.b64decode(res.json()['data'][len('data:application/octet-stream;base64,'):]) == data


'''
fin = open('/Users/cody/IdeaProjects/agent/mysql-connector-java-8.0.13.jar', 'rb').read()
params = urllib.parse.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})
headers = {"Content-type": "application/x-java-archive","Accept": "application/java-archive", "X-Auth-API-Service-Key":"BDB"}
conn = http.client.HTTPConnection("localhost",8181)
conn.request("POST", "/dashboard/plugins/uploadplugin", fin, headers)
response = conn.getresponse()
print(response.status, response.reason)
data = response.read()
conn.close()


conn = http.client.HTTPConnection("localhost",8181)
headers = {"X-Auth-API-Service-Key":"BDB"}
conn.request("GET", "/dashboard", headers={'X-Auth-API-Service-Key':'BDB'})
r1 = conn.getresponse()
print(r1.status, r1.reason)
data1 = r1.read()  # This will return entire content.
print(data1)
conn.close()
'''