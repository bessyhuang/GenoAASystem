import motor.motor_asyncio

from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

#APIRouter creates path operations for user module
router = APIRouter(
    prefix="/Generate_file",
    tags=["Generate_file"],
    responses={404: {"description": "Not found"}},
)


### Retrieve all documents in collection present in the database ###

# GET All Clinical Data (BaseModel) => `Response: dict`
@router.get("/")
async def GenerateFile_dashboard(request: Request):
    return templates.TemplateResponse("GenerateFile_dashboard.html", {"request": request})
