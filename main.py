from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from api import Survey_api, Respondent_api, Auth
from config.db import create_tables

create_tables()

app = FastAPI()
app.include_router(Survey_api.router)
app.include_router(Respondent_api.router)
app.include_router(Auth.router)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")
