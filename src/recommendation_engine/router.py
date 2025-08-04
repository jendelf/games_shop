from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from typing import List

from .pipeline.user_vectorizer import build_user_vector
from .pipeline.inference import inference

router = APIRouter()
templates = Jinja2Templates(directory="src/recommendation_engine/static/templates")

@router.get("/questionnare", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("questionnaire.html", {"request" : request})


@router.post("/submit")
async def get_answers(
    request: Request,
    game_mode: str = Form(...),
    genres: List[str] = Form(...),
    favourites: str = Form(...),
    genres_other: str = Form(None),
):
    user_vector = build_user_vector(game_mode, genres, favourites, genres_other)
    return inference(user_vector, 10)

#TODO в будущем заменить на js 