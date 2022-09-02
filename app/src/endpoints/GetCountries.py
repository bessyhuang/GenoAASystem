from fastapi import APIRouter
from fastapi import Query

from src.models.Countries import Country



#APIRouter creates path operations for user module
router = APIRouter(
    prefix="/Country",
    tags=["Country"],
    responses={404: {"description": "Not found"}},
)



### --- TEST: Get data from a dropdown menu with FastAPI --- ###
# Method 1
@router.get('/get_countries_v1')
async def get_countries(_q: str = Query("eu", enum=["eu", "us", "cn", "ru"])):
    return {"selected": _q}

# Method 2
@router.get("/get_countries_v2")
def get_something(country: Country = Country.eu):
    return {"country": country.value}
