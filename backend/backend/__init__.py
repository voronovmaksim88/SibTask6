from fastapi import APIRouter

from demo_auth.views import router as demo_auth_router

router = APIRouter()
router.include_router(router=demo_auth_router)
