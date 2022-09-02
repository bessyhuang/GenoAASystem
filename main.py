
import motor.motor_asyncio
import uvicorn
import json
import pprint

from fastapi import FastAPI
from bson import json_util
from bson.objectid import ObjectId
from pydantic import BaseModel, Field


###
from typing import Union
from typing import List

# Install Jinja2 Templates
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Import Form
from fastapi import Form
from src.model import spell_number


# Connect to MongoDB by using motor
MONGODB_INFO = "mongodb://10.64.16.166:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_INFO, serverSelectionTimeoutMS=5000)
db = client["FabryDisease"]


# Initialize FastAPI
app = FastAPI()

# Setting: static file
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setting: templates file
templates = Jinja2Templates(directory="templates")


### Select specific fields and display on FastAPI interface ###
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class ClinicalModel(BaseModel):
    #id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    #No: str = Field(alias="No")
    SampleID: str = Field(alias="SampleID")
    Group: str = Field(alias="Group")
    Age: str = Field(alias="Age")
    LVMI: str = Field(alias="LVMI")
    microalbumin: str = Field(alias="microalbumin")
    Gender: str = Field(alias="Gender")
    ERT_drugs: str = Field(alias="ERT drugs")
    IVSD_before_ERT: str = Field(alias="IVSD before ERT")
    #Treatment_in_other_hospitals: str = Field(alias="Treatment in other hospitals")
    #date_of_birth: str = Field(alias="date of birth")
    #ERT_start_date: str = Field(alias="ERT start date")
    Heart_MRI_LGE: str = Field(alias="Heart MRI LGE (fibrosis)")
    Remark: str = Field(alias="Remark")
    #Medical_Record_Number: str = Field(alias="Medical record number")
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

### Retrieve all documents in collection present in the database ###
# GET All Clinical Data (BaseModel) => `Response: dict`
@app.get("/dashboard_basemodel", response_description="Display All Clinical Data", response_model=ClinicalModel)
async def GetAllClinicalData():
    COLLECTION = "Clinical"
    document = await db[COLLECTION].find_one({})
    return document

# GET All Clinical Data (Not using BaseModel; 直接處理從 MongoDB Query 回來的結果，即把 Dict 轉為 Dict_JSON) => `Response: dict_JSON`
@app.get("/dashboard_json", response_description="Display All Clinical Data")
async def GetAllClinicalData():
    COLLECTION = "Clinical"
    document = await db[COLLECTION].find_one({})
    json_output = json.loads(json_util.dumps(document))
    return json_output

# GET All Clinical Data (BaseModel) + Jinja Template => `Response: list`
@app.get("/dashboard", response_description="Display All Clinical Data", response_model=ClinicalModel)
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


# Define Form parameters (GET, POST)
@app.get("/form")
def form_post(request: Request):
    result = "Type a number"
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})

@app.post("/form")
def form_post(request: Request, num: int = Form(...)):
    result = spell_number(num)
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})


# GET -> response JSON
#@app.get("/items/{item_id}")
#def read_item(item_id: int, q: Union[str, None] = None):
#    return {"item_id": item_id, "q": q}

# GET -> render on HTML template
@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", context={"request": request, "id": id})

# Query: Multiple parameters
@app.get("/search/clinicals")
async def search_clinicals(Age: Union[str, None] = None, LVMI: Union[str, None] = None, Group: Union[str, None] = None, ERT_drug: Union[str, None] = None):
    DISPLAYED_FIELD = { "_id": 0, "SampleID": 1, "Group": 1, "Age": 1, "LVMI": 1, "microalbumin": 1, "Gender": 1, "ERT drugs": 1, "IVSD before ERT": 1, "Heart MRI LGE (fibrosis)": 1, "Remark": 1 }
    #async for item in db.Clinical.find({}, DISPLAYED_FIELD):
    #    print(item)
    #json_docs = [json.dumps(doc, default=json_util.default) async for doc in db.Clinical.find({})]
    #return json_docs



if __name__ == "__main__":
    uvicorn.run(app='main:app', host="10.64.16.241", port=8000, reload=True, debug=True)
