import requests
import json
from bs4 import BeautifulSoup
userid='apikey'
passwd='8b61472ad3ccf78f384d489a3aeec1872d1078b0cd9a55170938f476bc9b0b23'
html_doc = requests.post(
    'http://192.168.99.100:30080/api/v3/users/',
    json.dumps({
    "login": "h.wurst",
    "email": "h.wurst@openproject.com",
    "firstName": "Hans",
    "lastName": "Wurst",
    "admin": "false",
    "language": "de",
    "status": "active",
    "password": "hunter5"
    }),
    headers={'Content-Type': 'application/hal+json'},
    auth=(userid, passwd)).text
soup = BeautifulSoup(html_doc, 'html.parser') # BeautifulSoup
print(soup.prettify())