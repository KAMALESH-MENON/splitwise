from fastapi import APIRouter

router = APIRouter(tags=["Reports and Analytics Routes"])


@router.get("/reports/test")
def testing():
    return {"message": "Hello World from reports!"}
