import logging
import os
import uuid
import datetime
import asyncio

logging.basicConfig(level=logging.INFO, format="%(asctime)s: %(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
logger = logging.getLogger("log-writer")

random_string = str(uuid.uuid4())

shared_file_path = os.getenv("SHARED_FILE_PATH", "/app/logs/logs.txt")

def ensure_file_exists():
    os.makedirs(os.path.dirname(shared_file_path), exist_ok=True)
    if not os.path.exists(shared_file_path):
        with open(shared_file_path, "w") as file:
            file.write("")
        logger.info(f"No file found, Created a new log file at: {shared_file_path}")

async def write_to_file():
    while True:
        current_timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        content = f"{current_timestamp}:{random_string}\n"
        with open(shared_file_path, "a") as file:
            file.write(content)
        await asyncio.sleep(5)

if __name__ == "__main__":
    ensure_file_exists()
    asyncio.run(write_to_file())