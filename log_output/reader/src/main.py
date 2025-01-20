import logging
import os
import hashlib
import requests
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger("Log Output App")

app = FastAPI()

shared_file_path = os.getenv("SHARED_FILE_PATH", "/app/logs/")
logs_path = "/app/logs/logs.txt"
file_path = "/app/config/information.txt"

def calculate_hash(content):
    return hashlib.sha256(content.encode()).hexdigest()

def read_file():
    try:
        with open(file_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")

        return "File not found"

@app.get("/")
def root(request: Request):
    return "Service is up", 200

@app.get("/status")
def read_logs():
    try:
        with open(logs_path, "r") as file:
            lines = file.readlines()
        if not lines:
            return JSONResponse(content={"error": "Log file is empty"}, status_code=404)
        latest = lines[-1].strip()
        file_content = read_file()
        env_var = os.getenv("MESSAGE", "Not found")

        try:
            response = requests.get("http://ping-pong-svc:80/pingpong")
            data = response.json()
            pingpongs = data.get("pong_count", 0)
        except requests.RequestException as error:
            logger.error(f"Error in requesting pongs from pingpong: {error}")

        return JSONResponse(
            content={
            "file_content": file_content,
            "env variable": env_var,
            "latest_log": latest,
            "ping / pongs": pingpongs},
            status_code=200,
        )
    except FileNotFoundError:
        return JSONResponse(content={"error": "Log file not found"}, status_code=404)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 3030)), log_level="trace")
