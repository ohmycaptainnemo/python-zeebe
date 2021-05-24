from fastapi import FastAPI
import uvicorn
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger()

if __name__ == "__main__":
    app = FastAPI(docs_url="/")

    with open("VERSION", "r") as f:
        VERSION = f.read()

    @app.get("/version")
    def version():
        return VERSION
    
    uvicorn.run(app, host="0.0.0.0", port=5555)
