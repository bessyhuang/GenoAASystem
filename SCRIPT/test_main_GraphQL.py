from fastapi import FastAPI
from typing import Union
import uvicorn
import motor.motor_asyncio

###
import strawberry
from strawberry.asgi import GraphQL

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
        "id": str(coll_clinical["_id"]), 
        "SampleID": coll_clinical["SampleID"],
        "Group": coll_clinical["Group"],
        "Age": coll_clinical["Age"],
        "date of birth": coll_clinical["date of birth"],
        "LVMI": coll_clinical["LVMI"],
        "ERT drugs": coll_clinical["ERT drugs"]
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


###
@strawberry.type
class User:
    name: str
    age: int

@strawberry.type
class Query:
    @strawberry.field
    def user(self) -> User:
        return User(name="Patrick", age=100)

schema = strawberry.Schema(query=Query)
graphql_app = GraphQL(schema)


@app.get("/")
def read_root():
    return {"Hello": "World"}

app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)


#@app.get("/items/{item_id}")
#def read_item(item_id: int, q: Union[str, None] = None):
#    return {"item_id": item_id, "q": q}

@app.get("/GET_coll", response_description="Clinical data retrieved")
async def get_coll():
    clincals = await retrieve_coll(COLLECTION)
    if clincals:
        return ResponseModel(clincals, "Data retrieved successfully")
    else:
        return ResponseModel(clincals, "Empty list returned")

if __name__ == "__main__":
    uvicorn.run(app='test_main:app', host="10.64.16.241", port=8000, reload=True, debug=True)
