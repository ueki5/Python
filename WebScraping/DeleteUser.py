import requests
import json
from bs4 import BeautifulSoup
import OpenProjectApi
opnprj=OpenProjectApi.OpenProjectApi()
soup=opnprj.delete('users', '41')
print(soup.prettify())