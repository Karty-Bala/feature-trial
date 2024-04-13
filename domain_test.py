from urllib.parse import urlparse

url = input("Enter url: ")
parsed_url = urlparse(url)
domain_name = parsed_url.netloc

print(domain_name)  # --> www.example.com
