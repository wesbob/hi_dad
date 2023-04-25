import requests
import json

url = "https://www.hi-dad.lol/api/posts"

response = requests.get(url)
print(response.status_code)

posts = json.loads(response.text)
print(posts)