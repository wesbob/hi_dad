import requests
import json


url = "http://127.0.0.1:5000/api/posts"
headers = {'API_KEY': 'd6736be5-c6d2-4b0a-b9a7-a266ff96cebe'}
response = requests.get(url, headers=headers)
print(response.status_code)



# for post in posts:
#     print(post['title'])
#     print(post['content'])
#     print(post['img'])
#     print(post['date_created'])
#     print('----------------------------------')
