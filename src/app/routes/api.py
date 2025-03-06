from fastapi import APIRouter

from app.routes.v1 import (
    expense_management_routers,
    group_management_routers,
    reports_and_analytics_routers,
    settlements_routers,
    user_management_routers,
    user_profile_routers,
)

router = APIRouter(prefix="/api/v1")

router.include_router(expense_management_routers.router)
router.include_router(group_management_routers.router)
router.include_router(reports_and_analytics_routers.router)
router.include_router(settlements_routers.router)
router.include_router(user_management_routers.router)
router.include_router(user_profile_routers.router)
