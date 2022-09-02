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
    prefix="/dashboard",
    tags=["Dashboard"],
    responses={404: {"description": "Not found"}},
)


### Retrieve all documents in collection present in the database ###

# GET All Clinical Data (BaseModel) => `Response: dict`
@router.get("/dashboard_basemodel", response_description="Display All Clinical Data", response_model=schemas.ClinicalModel)
async def GetAllClinicalData():
    COLLECTION = "Clinical"
    document = await db[COLLECTION].find_one({})
    return document

# GET All Clinical Data (Not using BaseModel; 直接處理從 MongoDB Query 回來的結果，即把 Dict 轉為 Dict_JSON) => `Response: dict_JSON`
@router.get("/dashboard_json", response_description="Display All Clinical Data")
async def GetAllClinicalData():
    COLLECTION = "Clinical"
    document = await db[COLLECTION].find_one({})
    json_output = json.loads(json_util.dumps(document))
    return json_output

# GET All Clinical Data (BaseModel) + Jinja Template => `Response: list`
@router.get("/", response_description="Display All Clinical Data", response_model=schemas.ClinicalModel)
async def GetAllClinicalData_jinja(request: Request):
    COLLECTION = "Clinical"
    cursor = db[COLLECTION]
    DISPLAYED_FIELD = { "_id": 0, "SampleID": 1, "Group": 1, "Age": 1, "LVMI": 1, "microalbumin": 1, "Gender": 1, "ERT drugs": 1, "IVSD before ERT": 1, "Heart MRI LGE (fibrosis)": 1, "Remark": 1 }
    clins = await cursor.find({}, DISPLAYED_FIELD).to_list(length=None)
    JSON_clins = json.loads(json.dumps(clins))
    LIST_key_clins = list(clins[0].keys())
    return templates.TemplateResponse("Clinical.html", context={"request": request, "clins": JSON_clins, "key_clins": LIST_key_clins})

    #async for document in cursor.find({}, DISPLAYED_FIELD):
    #    pprint.pprint(document)
    #    return document

    #print('clins: {} -> {}'.format(type(clins), type(JSON_clins)))
    #clins: <class 'list'> -> <class 'list'>

    #JSON_key_clins = json.dumps(key_clins)
    #print('key_clins: {} -> X {} X'.format(type(key_clins), type(JSON_key_clins)))
    #key_clins: <class 'list'> -> X <class 'str'> X
