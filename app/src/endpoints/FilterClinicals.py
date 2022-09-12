import motor.motor_asyncio
import json
import schemas

from bson import json_util
from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates

from typing import Union
from fastapi import Form

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


@router.get("/")
async def parameter_form(request: Request):
    return templates.TemplateResponse('InputForm.html', context={'request': request})

@router.post("/")
async def parameter_form(
    *, request: Request, 
    age: int = Form(...), LVMI: float = Form(...), 
    group: str = Form(...), ERT_drug: str = Form(...),
    response_model=schemas.ClinicalModel):
    
    results = {"age": age, "LVMI": LVMI, "group": group, "ERT_drug": ERT_drug}
    #return templates.TemplateResponse('FilteredFormResult.html', context={'request': request, 'result': results})

    COLLECTION = "Clinical"
    cursor = db[COLLECTION]
    DISPLAYED_FIELD = { "_id": 0, "SampleID": 1, "Group": 1, "Age": 1, "LVMI": 1, "microalbumin": 1, "Gender": 1, "ERT drugs": 1, "IVSD before ERT": 1, "Heart MRI LGE (fibrosis)": 1, "Remark": 1 }

    if results['ERT_drug'] == 'No selected':
        pipeline = [
            {'$match': {'Group': results['group']}},
            {'$match': {'Age':  { '$gte': results['age']}}},
            {'$match': {'LVMI': { '$gte': results['LVMI']}}},
            {'$project': DISPLAYED_FIELD}
        ]
    else:
        pipeline = [
            {'$match': {'Group': results['group']}},
            {'$match': {'Age':  { '$gte': results['age']}}},
            {'$match': {'LVMI': { '$gte': results['LVMI']}}},
            {'$match': {'ERT drugs': results['ERT_drug']}},
            {'$project': DISPLAYED_FIELD}
        ]

    #print(pipeline)
    LIST_clins = await cursor.aggregate(pipeline).to_list(length=None)
    print(LIST_clins)
    return templates.TemplateResponse("FilterClins.html", context={"request": request, "clins": LIST_clins})
