from asyncio.log import logger
from contextlib import asynccontextmanager
import logging
import os
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
import uvicorn
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger("TODO app")

HTML_FILE_PATH = "html/index.html"
CACHE_DIR = "/app/storage"
CACHE_FILE = os.path.join(CACHE_DIR, "cached_image.jpg")
CACHE_EXPIRATION = 60 * 60

@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(CACHE_DIR, exist_ok=True)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/", response_class=HTMLResponse)
async def root():
    try:
        with open(HTML_FILE_PATH, "r") as file:
            html_content = file.read()
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>HTML file not found</h1>", status_code=404)

def is_cache_valid():
    if not os.path.exists(CACHE_FILE):
        return False
    last_modified = os.path.getmtime(CACHE_FILE)
    return (time.time() - last_modified) < CACHE_EXPIRATION


def fetch_random_image():
    try:
        response = requests.get("https://picsum.photos/1200", stream=True)
        response.raise_for_status()
        with open(CACHE_FILE, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching image: {e}")

@app.get("/random-image")
async def get_random_image():
    if not is_cache_valid():
        fetch_random_image()
    return FileResponse(CACHE_FILE, media_type="image/jpeg")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)), log_level="trace")