from fastapi import APIRouter


router = APIRouter()


@router.get("/version")
def version():
    with open("VERSION", "r") as f:
        VERSION = f.read()
    return VERSION
