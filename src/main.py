import asyncio
from asyncio.log import logger
import logging
import os
import uuid
from fastapi import FastAPI
import uvicorn

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)
random_uuid = uuid.uuid4()

PORT = int(os.getenv("PORT", 8080))

async def log_uuid():
    while True:
        logger.info(f"UUID: {random_uuid}")
        await asyncio.sleep(5)

async def lifespan(app: FastAPI):
    logger.info("Starting background task")
    task = asyncio.create_task(log_uuid())

    yield 

    logger.info("Stopping background task")
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        logger.info("Background task stopped")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": f"Server is running on port {PORT}"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    logger.info(f"Server started on port {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)