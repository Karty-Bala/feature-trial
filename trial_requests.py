import requests

url = str(input("enter url: "))
result = requests.get("https://website-categorization.whoisxmlapi.com/api/v2?apiKey=at_Xvchfwv7SVhPs9JPN0he6PVzzZPge&domainName=" + url)
print((result.content).decode('ascii'))