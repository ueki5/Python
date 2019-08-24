import requests
import json
from bs4 import BeautifulSoup
userid='apikey'
passwd='34739f806ab1b3caa301a77871a35600c1470ac8b13187bdb8b0c5fa1cad0404'
url='http://192.168.99.100:30080/api/v3/work_packages/'
workpkg_id='42'
html_doc = requests.delete(url + workpkg_id, headers={'Content-Type': 'application/hal+json'}, auth=(userid, passwd)).text
soup = BeautifulSoup(html_doc, 'html.parser') # BeautifulSoup
print(soup.prettify())