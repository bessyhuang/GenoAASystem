from fastapi import APIRouter
from fastapi import Request, Form
from fastapi.templating import Jinja2Templates

# Import custom schemas & functions
from src.models.SpellNumber import spell_number



templates = Jinja2Templates(directory="app/templates")


#APIRouter creates path operations for user module
router = APIRouter(
    prefix="/spell_number_form",
    tags=["SpellNumberForm"],
    responses={404: {"description": "Not found"}},
)


### --- TEST: Define Form parameters (GET, POST) --- ###
@router.get("/form")
def form_post(request: Request):
    result = "Type a number"
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})

@router.post("/form")
def form_post(request: Request, num: int = Form(...)):
    result = spell_number(num)
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})
