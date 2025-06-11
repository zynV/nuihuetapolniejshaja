from fastapi import FastAPI
from web.oauth_callback import router as oauth_router
from database.db import init_db

init_db()

app = FastAPI()
app.include_router(oauth_router)

