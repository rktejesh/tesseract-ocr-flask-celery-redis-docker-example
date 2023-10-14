# This file test /image endpoint (POST request) - Asynchronous OCR processing using Celery. Returns a task ID.

import requests
import base64

# Open image and encode to base64
with open('sample3.png', 'rb') as f:
    image_encoded = base64.b64encode(f.read()).decode('utf-8')

# Post to the /image endpoint to start the task
response = requests.post('http://localhost:5001/image', json={'image_data': image_encoded, 'name': 'hello'})
data = response.json()
print(data)  # Should display the task ID


print("You will need this task ID for running test3.py")
