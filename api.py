import uvicorn
import logging

from src.api import app
from src.zeebe.settings import PORT

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger()

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=PORT, reload=True)
