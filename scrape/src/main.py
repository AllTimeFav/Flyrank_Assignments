import requests


url = "https://books.toscrape.com/robots.txt"   

# Send request
response = requests.get(url)

print(response.text)
