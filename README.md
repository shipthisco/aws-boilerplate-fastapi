# FastAPI Google Cloud Example

This project demonstrates a FastAPI application integrating Google Cloud Storage, Cloud Tasks, MongoDB, and Redis.

## Features
- Upload files to Google Cloud Storage via `/upload`.
- Enqueue processing tasks using Cloud Tasks.
- Store metadata in MongoDB and cache in Redis.
- Retrieve metadata via `/files/{filename}`.
- Dockerized for deployment.
