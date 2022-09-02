from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Union


templates = Jinja2Templates(directory="app/templates")


#APIRouter creates path operations for user module
router = APIRouter(
    prefix="/items",
    tags=["Items"],
    responses={404: {"description": "Not found"}},
)


# GET -> response JSON
@router.get("/items_v1/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# GET -> render on HTML template
@router.get("/items_v2/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", context={"request": request, "id": id})
