import requests
import json
from bs4 import BeautifulSoup
import OpenProjectApi
data=json.dumps(
    {
    "login": "ueki7",
    "email": "ueki7@fujitsu.com",
    "firstName": "7",
    "lastName": "ueki",
    "admin": "false",
    "language": "ja",
    "status": "active",
    "password": "ueki5555"
    })
opnprj=OpenProjectApi.OpenProjectApi()
soup=opnprj.create('users', data)
print(soup.prettify())