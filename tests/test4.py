# This file test /get-tasks endpoint (GET request) - Fetches the result of an asynchronous OCR task given its task ID.

import requests

response = requests.get('http://127.0.0.1:5000/get-tasks')
data = response.json()
print(data)