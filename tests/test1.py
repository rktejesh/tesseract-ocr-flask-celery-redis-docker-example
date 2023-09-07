# This file tests "/image-sync" endpoint (POST request) - Synchronous OCR processing.

import requests
import base64

# Open image and encode to base64
with open('temo.crop.png', 'rb') as f:
    image_encoded = base64.b64encode(f.read()).decode('utf-8')

response = requests.post('http://localhost:5001/image-sync', json={'image_data': image_encoded})
print(response.json())