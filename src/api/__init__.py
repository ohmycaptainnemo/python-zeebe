import logging
from fastapi import FastAPI


from .heartbeat_router import router as heartbeat
from .zeebe_router import router as zeebe

app = FastAPI(
    version="0.1.0",
    title="Zeebe Sandbox",
    description="An API to allow experimenting with workflows and demonstrating Zeebe functionality.",
    docs_url="/",
)


app.include_router(heartbeat, prefix="/hearbeat", tags=["heartbeat"])
app.include_router(zeebe, prefix="/zeebe", tags=["zeebe"])
