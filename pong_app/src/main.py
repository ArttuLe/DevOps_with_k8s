import logging
import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

pong_state = {"pong": 0}
pong = 0

app = FastAPI()

@app.get("/")
def root():
    return {"message": "pong app"}

@app.get("/pingpong")
def status():
    pong_state["pong"] += 1
    return JSONResponse(
        content={"pong": pong_state["pong"]},
        status_code=200,
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 3030)), log_level="trace")