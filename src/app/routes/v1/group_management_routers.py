from fastapi import APIRouter

router = APIRouter(tags=["Group Management Routes"])


@router.get("/groups/test")
def testing():
    return {"message": "Hello World from group!"}
