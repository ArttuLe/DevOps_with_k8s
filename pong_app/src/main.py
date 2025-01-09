import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

pong_state = {"pong": 0}
pong = 0
shared_file_path = os.getenv("SHARED_FILE_PATH", "/app/logs/")
pong_path = shared_file_path + "pongs.txt"

app = FastAPI()

@app.get("/")
def root():
    return {"message": "pong app"}

@app.get("/pingpong")
def status():
    pong_state["pong"] += 1
    with open(pong_path, "a") as file:
        file.write(str(pong_state["pong"])+"\n")
    return JSONResponse(
        content={"pong": pong_state["pong"]},
        status_code=200,
    )

if __name__ == "__main__":
    def ensure_file_exists():
        os.makedirs(os.path.dirname(pong_path), exist_ok=True)
        if not os.path.exists(pong_path):
            with open(pong_path, "w") as file:
                file.write("")
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 3030)), log_level="trace")