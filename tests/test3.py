# This file test /image endpoint (GET request) - Fetches the result of an asynchronous OCR task given its task ID.

import requests
import time

task_id = "2cd8d48f-f301-4173-a0a7-334d6ec1d502" # Enter any task ID that you got after running test2.py file.

while True:
    response = requests.get('http://127.0.0.1:5000/image', json={'task_id': task_id})
    data = response.json()

    if 'text' in data:
        print(data['text'])  # This should display the OCR result
        break
    else:
        print("Task is still processing. Waiting...")
        time.sleep(2)  # Wait for 2 seconds before polling again
