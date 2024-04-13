import websitecategorization
from websitecategorization import Client

client = Client('at_Xvchfwv7SVhPs9JPN0he6PVzzZPge')

# Get categories for a domain name.
# response = client.data('whoisxmlapi.com')
url = str(input())
response = client.data(url)
print("Responded? " + "Yes" if response.website_responded else "No")
if response.website_responded:
    for cat in response.categories:
        print("Cat: " + str(cat.name))

# Specifying minimal level of confidence
# Getting raw API response in XML
xml = client.raw_data(url, output_format=Client.XML_FORMAT)
print(xml)