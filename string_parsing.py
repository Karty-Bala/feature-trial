import json
from urllib.parse import urlparse
import requests


def get_domain_name(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain.startswith('www.'):
        domain = domain[4:]
    return domain


url = input("enter url: ")
domain_name = get_domain_name(url)
print("Domain name:", domain_name)
result = requests.get("https://website-categorization.whoisxmlapi.com/api/v3?apiKey=at_Xvchfwv7SVhPs9JPN0he6PVzzZPge&domainName=" + domain_name)

str_json = result.content.decode('ascii')
print("api works", str_json)


data = json.loads(str_json)
categories = data.get('categories', [])
listCategories = []

for category in categories:

    name = category.get('name', '')
    confidence = category.get('confidence', 0)
    listCategories.append({"name": name, "confidence": int(confidence * 100)})

for ctgry in listCategories:
    print("Name:" + ctgry['name'] + " Confidence:" + str(int(ctgry['confidence'])))
