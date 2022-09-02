from fastapi import APIRouter
from src.endpoints import SpellNumberForm

router = APIRouter()
router.include_router(SpellNumberForm.router)
