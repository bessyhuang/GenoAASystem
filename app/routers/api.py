from fastapi import APIRouter
from src.endpoints import SpellNumberForm, Dashboard, Items, GetCountries



router = APIRouter()
router.include_router(SpellNumberForm.router)
router.include_router(Dashboard.router)
router.include_router(Items.router)
router.include_router(GetCountries.router)
