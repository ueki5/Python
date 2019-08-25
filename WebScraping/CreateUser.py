import requests
import json
from bs4 import BeautifulSoup
userid='apikey'
passwd='34739f806ab1b3caa301a77871a35600c1470ac8b13187bdb8b0c5fa1cad0404'
auth=(userid, passwd)
urlbase='http://192.168.99.100:30080/api/v3/'
subdir='users/'
objid=''
url=urlbase+subdir+objid
headers={'Content-Type': 'application/json'}
data=json.dumps(
    {
    "login": "ueki6",
    "email": "ueki6@fujitsu.com",
    "firstName": "6",
    "lastName": "ueki",
    "admin": "false",
    "language": "ja",
    "status": "active",
    "password": "ueki5555"
    })
html_doc = requests.post(url, data, headers=headers, auth=auth).text
soup = BeautifulSoup(html_doc, 'html.parser') # BeautifulSoup
print(soup.prettify())