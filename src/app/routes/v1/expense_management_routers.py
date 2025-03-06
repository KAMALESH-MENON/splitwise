from fastapi import APIRouter

router = APIRouter(tags=["Expense Management Routes"])


@router.get("/expense/test")
def testing():
    return {"message": "Hello World from !"}
