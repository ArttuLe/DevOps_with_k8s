import logging
import os
import uuid
import datetime
import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

logging.basicConfig(level=logging.INFO, format="%(asctime)s: %(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
logger = logging.getLogger("log-output")

random_string = str(uuid.uuid4())
current_timestamp = datetime.datetime.now(datetime.timezone.utc)

async def log_output():
    global current_timestamp
    while True:
        current_timestamp = datetime.datetime.now(datetime.timezone.utc)
        logger.info(f"{current_timestamp}: {random_string}")
        await asyncio.sleep(5)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting the log-output app")
    log_task = asyncio.create_task(log_output())
    try:
        yield
    finally:
        logger.info("Stopping the log-output app")
        log_task.cancel()
        try:
            await log_task
        except asyncio.CancelledError:
            logger.info("Background task stopped")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "log-output application"}

@app.get("/status")
def status():
    return JSONResponse(
        content={"timestamp": current_timestamp.isoformat(), "string": random_string},
        status_code=200,
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 3000)), log_level="trace")