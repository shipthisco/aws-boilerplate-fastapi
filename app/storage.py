import os
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')

storage_client = storage.Client()
bucket = storage_client.bucket(GCS_BUCKET_NAME)

def upload_file(file_data: bytes, destination_blob_name: str) -> str:
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(file_data)
    blob.make_public()
    return blob.public_url
