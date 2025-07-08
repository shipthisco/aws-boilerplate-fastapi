import os
import json
from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

PROJECT = os.getenv('GCT_PROJECT')
LOCATION = os.getenv('GCT_LOCATION')
QUEUE = os.getenv('GCT_QUEUE')
CALLBACK_URL = os.getenv('GCT_CALLBACK_URL')

client = tasks_v2.CloudTasksClient()
parent = client.queue_path(PROJECT, LOCATION, QUEUE)

def enqueue_task(payload: dict):
    task = {
        'http_request': {
            'http_method': tasks_v2.HttpMethod.POST,
            'url': CALLBACK_URL,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(payload).encode()
        }
    }
    # Optional: schedule in the future. Here we send immediately
    response = client.create_task(request={'parent': parent, 'task': task})
    return response.name
