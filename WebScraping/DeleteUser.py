import requests
import json
from bs4 import BeautifulSoup
userid='apikey'
passwd='34739f806ab1b3caa301a77871a35600c1470ac8b13187bdb8b0c5fa1cad0404'
auth=(userid, passwd)
urlbase='http://192.168.99.100:30080/api/v3/'
subdir='users/'
objid='39'
url=urlbase+subdir+objid
headers={'Content-Type': 'application/json'}
html_doc = requests.delete(url, headers=headers, auth=auth).text
soup = BeautifulSoup(html_doc, 'html.parser') # BeautifulSoup
print(soup.prettify())