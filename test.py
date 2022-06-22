import requests

BASE = 'http://127.0.0.1:5000/'

# put request allows you to add in request data to the request
# this would be better if it was a post request

data = [{"likes": 78, "name": "Joe", "views": 100000},
        {"likes": 10000, "name": "How to make REST API", "views": 80000},
        {"likes": 35, "name": "Tim", "views": 2000}]

for i in range(len(data)):
  response = requests.put(BASE + 'video/' + str(i), data[i])
  print(response.json())

input()
response = requests.patch(BASE + 'video/2', {'views': 99})
print(response.json())

input()
response = requests.delete(BASE + 'video/2')
print(response)

input()
response = requests.get(BASE + 'video/2')
print(response.json())