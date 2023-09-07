from flask import Flask, request, jsonify
from celery import Celery
from PIL import Image
import pytesseract
from  preprocessing import pre_processing
import base64
import cv2
import io
import os
import numpy as np
import redis
from worker import celery

app = Flask(__name__)

# @celery.task(bind=True)
# def ocr_task(self, image_data):
#     img = Image.open(io.BytesIO(base64.b64decode(image_data)))
#     processed_img = pre_processing(img)
#     return pytesseract.image_to_string(processed_img)

@app.route('/image-sync', methods=['POST'])
def image_sync():
    image_data = request.json['image_data']
    img = Image.open(io.BytesIO(base64.b64decode(image_data)))
    processed_img = pre_processing(img)
    text = pytesseract.image_to_string(processed_img)
    return jsonify({"text": text})

@app.route('/image', methods=['POST'])
def image():
    image_data = request.json['image_data']
    # task = ocr_task.apply_async([image_data])
    task = celery.send_task('tasks.ocr_task', args=[image_data], kwargs={})
    return jsonify({"task_id": task.id})

@app.route('/image', methods=['GET'])
def get_image():
    task_id = request.json['task_id']
    task = celery.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'task_id': None,
        }
    else:
        response = {
            'text': task.info,
        }
    return jsonify(response)

@app.route('/get-tasks', methods=['GET'])
def get_tasks():
    r = redis.from_url('redis://redis:6379/0')
    keys = r.keys(pattern="celery-task-meta*")
    res = {}
    res["keys"] = []
    for element in keys:
        res["keys"].append(element.decode("utf-8").replace("celery-task-meta-", ""))
    return jsonify(res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
