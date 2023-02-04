

from fastapi import FastAPI

from .db import engine
from .func import utils
from .models import models
from .routes import users

models.Base.metadata.create_all(bind=engine)
#    .create_all(bind=engine)



app = FastAPI()


app.include_router(users.router)


@app.get("/")
def read_root():
    return {"Message": "Testing API"}



