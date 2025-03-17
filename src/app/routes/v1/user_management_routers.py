from fastapi import APIRouter

router = APIRouter(tags=["User Management Routes"])


@router.get("/register/test")
def testing():
    return {"message": "Hello World from settle-up!"}
