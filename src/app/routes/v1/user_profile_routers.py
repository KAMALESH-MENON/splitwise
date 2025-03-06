from fastapi import APIRouter

router = APIRouter(tags=["User Profile Routes"])


@router.get("/profile/test")
def testing():
    return {"message": "Hello World from profile!"}
