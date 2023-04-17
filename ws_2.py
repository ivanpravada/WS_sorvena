import json
from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()


@app.post("/manage")
def manage_post():
    return {"manage_post": "OK"}


@app.delete("/manage")
def manage_delete():
    return {"manage_delete": "OK"}
