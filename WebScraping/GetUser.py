
import requests
import json
from bs4 import BeautifulSoup
import OpenProjectApi
opnprj=OpenProjectApi.OpenProjectApi()
soup=opnprj.get('users', '')
print(soup.prettify())