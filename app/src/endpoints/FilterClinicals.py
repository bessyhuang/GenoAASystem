import motor.motor_asyncio
import os
import json
import schemas

from bson import json_util
from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates

from typing import Union, Optional
from fastapi import Form, Body
from pydantic import BaseModel

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
    #print(LIST_clins)
    return templates.TemplateResponse("FilterClins.html", context={"request": request, "clins": LIST_clins})


InputFilePath = "/home/tsailab/GenoAASystem/GAAsystem_input/"
OutputFilePath = "/home/tsailab/GenoAASystem/GAAsystem_output/"

@router.post("/Get_CaseControl_field")
async def Get_CaseControl_field(request: Request, CaseControl_info: list):
    #print('---', type(CaseControl_info), CaseControl_info, len(CaseControl_info))
    #print(CaseControl_info[0], CaseControl_info[1])
    with open(InputFilePath + 'CaseControl.txt', 'w') as f:
        for doc in CaseControl_info:
            print(doc.items(), type(doc), doc.keys())
            # dict_items([('name', 'DPFWGS005-60'), ('value', 'Control')])
            SampleID = list(doc.items())[0][1]
            CaseControl = list(doc.items())[1][1]
            f.write(SampleID + '\t' + CaseControl + '\n')

    # Sort: Case first, Control second.
    os.system("sort -k 2 GAAsystem_input/CaseControl.txt > GAAsystem_input/NEW_CaseControl.txt")
    os.system("awk -F '\t' '{print $1}' GAAsystem_input/NEW_CaseControl.txt > NEW_FabrySamples.list")

    # Merge (Option: reheader)
    os.system("bash 2.Merge_all_vcf_for_Whole-Samples-In-One-File.sh {}NEW_FabrySamples.list /NovaSeq_127/FabryDisease/WGS/Parabricks/hg38/filtered_VCF/ {}".format(InputFilePath, OutputFilePath))

    # Plink: make bfile & .ped & .info

    df = {"input_info": CaseControl_info}
    return {"msg": df}
