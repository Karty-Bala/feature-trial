import json
from urllib.parse import urlparse
import requests


def get_domain_name(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain


url = str(input("enter url: "))
domain_name = get_domain_name(url)
print(domain_name)
webCatURL = "https://website-categorization.whoisxmlapi.com/api/v2?apiKey=at_Xvchfwv7SVhPs9JPN0he6PVzzZPge&domainName="
geoLocURL = "https://ip-geolocation.whoisxmlapi.com/api/v1?apiKey=at_Xvchfwv7SVhPs9JPN0he6PVzzZPge&domain="
domRepURL = "https://domain-reputation.whoisxmlapi.com/api/v2?apiKey=at_Xvchfwv7SVhPs9JPN0he6PVzzZPge&domainName="

domRepresult = requests.get( domRepURL + domain_name)
domRep_data = json.loads(domRepresult.content.decode('ascii'))
print(domRep_data)

warning_descriptions = []
repScore = domRep_data["reputationScore"]
ssl_vulnerabilities_index = None
for index, result in enumerate(domRep_data["testResults"]):
    if result["test"] == "SSL vulnerabilities":
        ssl_vulnerabilities_index = index
        # Append warning descriptions to the list
        for warning in result["warnings"]:
            warning_descriptions.append(warning["warningDescription"])
        break
print(warning_descriptions)
# ssl_warnings = domRep_data["testResults"][2]["warnings"]  # Assuming SSL vulnerabilities are always at index 2
# domRepList = []
# print("Warning Descriptions of SSL Vulnerabilities:")
# for warning in ssl_warnings:
#     # print("-", warning["warningDescription"])
#     domRepList.append(warning["warningDescription"])
# rep_score = domRep_data["reputationScore"]

# geoLocresult = requests.get( geoLocURL + domain_name)
# loca_data = json.loads(geoLocresult.content.decode('ascii'))
# # print((result.content).decode('ascii'))
#
# print("Country:", loca_data["location"]["country"])
# print("Region:", loca_data["location"]["region"])

