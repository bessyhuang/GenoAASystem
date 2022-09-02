import uvicorn
import pprint
import json

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from typing import Union

# Import custom schemas & routers
import schemas
from routers.api import router as api_router



app = FastAPI()
app.mount("/static", StaticFiles(directory="./app/static"), name="static")



# Include routers
app.include_router(api_router)


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
