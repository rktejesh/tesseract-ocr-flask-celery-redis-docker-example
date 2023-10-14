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
# r = redis.from_url('redis://redis:6379/0')
r = redis.Redis(host='redis', port=6379, decode_responses=True)

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
    name = request.json['name']
    task = celery.send_task('tasks.ocr_task', args=[image_data], kwargs={})
    r.set(str(task.id), name)
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
    keys = r.keys(pattern="celery-task-meta*")
    res = {}
    for element in keys:
        taskid = element.replace("celery-task-meta-", "")
        name = r.get(str(taskid))
        res[name] = str(taskid)

    return jsonify(res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
