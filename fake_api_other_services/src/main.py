
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from core.config import settings

from pydantic import BaseModel
from faker import Faker


class UserInfo(BaseModel):
    user_id: str


class FilmInfo(BaseModel):
    film_id: str


fake = Faker()

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.post("/api/v1/user_info")
def user_info(user: UserInfo):
    return {"id": user.user_id, "email": fake.email(), "name": fake.name()}


@app.post("/api/v1/film_info")
def film_info(film: FilmInfo):
    return {"film_id": film.film_id, "title": fake.text(20)}



if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=settings.fake_app_port,
        reload=True,
    )

