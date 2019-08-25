
import requests
import json
from bs4 import BeautifulSoup
import OpenProjectApi
data=json.dumps(
    {
        "firstName": "ろくさん",
        "lockVersion":0
    })
opnprj=OpenProjectApi.OpenProjectApi()
soup=opnprj.update('users', '39', data)
print(soup.prettify())