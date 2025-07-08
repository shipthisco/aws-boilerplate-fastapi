import json
from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime
from .storage import upload_file
from .database import uploads_collection
from .tasks import enqueue_task
from .cache import redis_client

router = APIRouter()

@router.post('/upload')
async def upload(file: UploadFile = File(...)):
    data = await file.read()
    try:
        gcs_url = upload_file(data, file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    metadata = {
        'filename': file.filename,
        'gcs_url': gcs_url,
        'upload_time': datetime.utcnow().isoformat(),
        'status': 'uploaded'
    }
    await uploads_collection.insert_one(metadata)
    await redis_client.set(file.filename, json.dumps(metadata))
    enqueue_task(metadata)
    return {'gcs_url': gcs_url}

@router.post('/task-callback')
async def task_callback(data: dict):
    filename = data.get('filename')
    if not filename:
        raise HTTPException(status_code=400, detail='filename required')
    await uploads_collection.update_one({'filename': filename}, {'$set': {'status': 'processed'}})
    metadata = await uploads_collection.find_one({'filename': filename}, {'_id': 0})
    if metadata:
        await redis_client.set(filename, json.dumps(metadata))
    return {'status': 'updated'}

@router.get('/files/{filename}')
async def get_file_metadata(filename: str):
    cached = await redis_client.get(filename)
    if cached:
        return json.loads(cached)
    metadata = await uploads_collection.find_one({'filename': filename}, {'_id': 0})
    if not metadata:
        raise HTTPException(status_code=404, detail='Not found')
    await redis_client.set(filename, json.dumps(metadata))
    return metadata
