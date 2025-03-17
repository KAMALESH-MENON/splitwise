from fastapi import APIRouter

router = APIRouter(tags=["Settlements Routes"])


@router.get("/settle-up/test")
def testing():
    return {"message": "Hello World from settle-up!"}
