import os
import time
from celery import Celery
from PIL import Image
import io
import base64
import pytesseract
from  preprocessing import pre_processing

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

# @celery.task(bind=True)
# def ocr_task(self, image_data):
#     img = Image.open(io.BytesIO(base64.b64decode(image_data)))
#     processed_img = pre_processing(img)
#     return pytesseract.image_to_string(processed_img)