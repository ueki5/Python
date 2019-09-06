import requests
import json
from bs4 import BeautifulSoup
import OpenProjectApi
opnprj=OpenProjectApi.OpenProjectApi()
soup=opnprj.delete('work_packages', '48')
print(soup.prettify())