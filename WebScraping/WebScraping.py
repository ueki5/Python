import requests
from bs4 import BeautifulSoup
html_doc = requests.get("http://192.168.99.100:30080/api/v3/work_packages/").text
soup = BeautifulSoup(html_doc, 'html.parser') # BeautifulSoup
print(soup.prettify())

# # TODO1
# real_page_tags = soup.find_all("a")
# for tag in real_page_tags:
#     print(tag)

# # TODO2

# for tag in real_page_tags:
#     print(tag.string)
# # TODO3

# for tag in real_page_tags:
#     print(tag.get("href"))