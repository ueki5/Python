import requests
import json
from bs4 import BeautifulSoup
import OpenProjectApi
data=json.dumps(
    {
        "subject":"暫定の仕事！！",
        "lockVersion":0
    })
opnprj=OpenProjectApi.OpenProjectApi()
soup=opnprj.update('work_packages', '47', data)
print(soup.prettify())