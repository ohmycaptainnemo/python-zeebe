import uvicorn


from src.api import app
from src.zeebe.settings import PORT

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=PORT, reload=True)
