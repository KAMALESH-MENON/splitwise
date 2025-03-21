from fastapi import APIRouter

from src.app.routes.v1 import (
    activity_api,
    expense_management_routers,
    group_management_routers,
    user_management_routers,
    user_profile_routers,
)

router = APIRouter(prefix="/api/v1")

router.include_router(expense_management_routers.router)
router.include_router(group_management_routers.router)
router.include_router(activity_api.router)
router.include_router(user_management_routers.router)
router.include_router(user_profile_routers.router)
