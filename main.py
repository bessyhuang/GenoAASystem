from fastapi import FastAPI
from typing import Union
import uvicorn
import motor.motor_asyncio

# Install Jinja2 Templates
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


MONGODB_INFO = "mongodb://10.64.16.166:27017"
DATABASE = "FabryDisease"
COLLECTION = "Clinical"


# 1. Connect to MongoDB by using motor
def get_server_info(MONGODB_INFO):
    # replace this with your MongoDB connection string
    conn_str = MONGODB_INFO
    # set a 5-second connection timeout
    client = motor.motor_asyncio.AsyncIOMotorClient(conn_str, serverSelectionTimeoutMS=5000)
    try:
        print(client.server_info())
    except Exception:
        print("Unable to connect to the server.")
    return client

# 2. Select specific fields and display on FastAPI interface 
def coll_helper(coll_clinical) -> dict:
    # return specific fields as key:value pair
    return { 
        #"No": coll_clinical["No"],
        #"id": str(coll_clinical["_id"]),
        #"date of birth": coll_clinical["date of birth"],
        #"ERT start date": coll_clinical["ERT start date"],
        #"Treatment in other hospitals": coll_clinical["Treatment in other hospitals"],
        "SampleID": coll_clinical["SampleID"],
        "Group": coll_clinical["Group"],
        "Gender": coll_clinical["Gender"],
        "Age": coll_clinical["Age"],
        "IVSD before ERT": coll_clinical["IVSD before ERT"],
        "LVMI": coll_clinical["LVMI"],
        "ERT drugs": coll_clinical["ERT drugs"],
        "microalbumin": coll_clinical["microalbumin"],
        "Heart MRI LGE (fibrosis)": coll_clinical["Heart MRI LGE (fibrosis)"],
        "Remark": coll_clinical["Remark"],
    }

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

# 3. Retrieve all documents in collection present in the database
async def retrieve_coll(COLLECTION):
    new_coll = []
    collection = db.get_collection(COLLECTION)
    async for coll in collection.find():
        new_coll.append(coll_helper(coll))
    return new_coll


client = get_server_info(MONGODB_INFO)
db = client[DATABASE]
app = FastAPI()

# Setting: static file
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setting: templates file
templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root():
    return {"Hello": "World"}



#@app.get("/items/{item_id}")
#def read_item(item_id: int, q: Union[str, None] = None):
#    return {"item_id": item_id, "q": q}

# Add
@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})


# Fix
@app.get("/GET_coll", response_description="Clinical data retrieved")
async def get_coll(request: Request):
    clins = await retrieve_coll(COLLECTION)
    key_clins = list(clins[0].keys())
    if clins:
        #return ResponseModel(clins, "Data retrieved successfully")
        return templates.TemplateResponse("Clinical.html", {"request": request, "clins": clins, "key_clins": key_clins})
    else:
        return ResponseModel(clincals, "Empty list returned")


if __name__ == "__main__":
    uvicorn.run(app='main:app', host="10.64.16.241", port=8000, reload=True, debug=True)
