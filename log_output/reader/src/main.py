import os
import hashlib
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

shared_file_path = os.getenv("SHARED_FILE_PATH", "/app/logs/")
logs_path = shared_file_path + "logs.txt"
pong_path = shared_file_path + "pongs.txt"

def calculate_hash(content):
    return hashlib.sha256(content.encode()).hexdigest()

@app.get("/status")
def read_logs():
    try:
        with open(logs_path, "r") as file:
            lines = file.readlines()
        if not lines:
            return JSONResponse(content={"error": "Log file is empty"}, status_code=404)
        latest = lines[-1].strip()

        with open(pong_path, "r") as pong_file:
            pongs = pong_file.readlines()
            if not pongs:
                return JSONResponse(content={"error": "Ping Pong Log file is empty"}, status_code=404)
        pingpongs = pongs[-1].strip()
        return JSONResponse(
            content={
            "latest_log": latest,
            "ping / pongs": pingpongs},
            status_code=200,
        )
    except FileNotFoundError:
        return JSONResponse(content={"error": "Log file not found"}, status_code=404)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 3000)), log_level="trace")
