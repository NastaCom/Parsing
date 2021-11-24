import requests
import json


url = 'https://api.github.com'
user = 'SergeyOS'

response = requests.get(f'{url}/users/{user}/repos')

for i in response.json():
    print(i['name'])

with open('lesson_1.json', 'w') as j:
    json.dump(response.json(), j)
