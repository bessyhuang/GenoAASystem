import motor.motor_asyncio
import json
import schemas

from bson import json_util
from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates



templates = Jinja2Templates(directory="app/templates")


# Connect to MongoDB by using motor
MONGODB_INFO = "mongodb://10.64.16.166:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_INFO, serverSelectionTimeoutMS=5000)
db = client["FabryDisease"]


#APIRouter creates path operations for user module
router = APIRouter(
    prefix="/filter",
    tags=["Filter"],
    responses={404: {"description": "Not found"}},
)


### Retrieve all documents in collection present in the database ###

# GET All Clinical Data (BaseModel) => `Response: dict`
@router.get("/clinical", response_model=schemas.ClinicalModel)
async def FilterClinicals(request: Request):
    COLLECTION = "Clinical"
    cursor = db[COLLECTION]
    pipeline = [{"$match": {'Group': '非ERT組'}}]

    LIST_clins = await cursor.aggregate(pipeline).to_list(length=None)
    return templates.TemplateResponse("FilterClins.html", context={"request": request, "clins": LIST_clins})
