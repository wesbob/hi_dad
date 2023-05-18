import requests
import json


url = "https://www.hi-dad.lol/api/posts"
headers = {'API_KEY': "poopybutthole"}
response = requests.get(url, headers=headers)
print(response)



# for post in posts:
#     print(post['title'])
#     print(post['content'])
#     print(post['img'])
#     print(post['date_created'])
#     print('----------------------------------')
