import requests
import json
from pydantic import BaseModel
from fastapi import FastAPI, Request, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI()

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "password": "secret",
    },
    "alice": {
        "username": "alice",
        "password": "secret2",
    },
}

WS1_URL = 'http://localhost:8001/'
WS2_URL = 'http://localhost:8002/'

security = HTTPBasic()


class ItemWS1CountGoods(BaseModel):
    title: str
    count: int


class ItemWS2(BaseModel):
    title: str
    price: int


def get_current_user(username):

    if username in fake_users_db:
        return fake_users_db[username]

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Check the login and password",
                        headers={"WWW-Authenticate": "Basic"})


def validate_credentials(credentials: HTTPBasicCredentials = Depends(security)):

    user = get_current_user(credentials.username)

    if not credentials.password == user["password"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Check the login and password",
                            headers={"WWW-Authenticate": "Basic"})
    return user


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return HTMLResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content="Check request parameters"
    )


@app.get("/get_goods")
def get_goods(product: Request):
    client_query = product.url.query
    if client_query:
        url = WS1_URL + 'goods?' + client_query
    else:
        url = WS1_URL + 'goods'

    try:
        req = requests.get(url=url)
    except requests.exceptions.ConnectionError as e:
        return "WS_1 offline -- try later"
    return req.json()


@app.post("/count_goods")
def count_goods(item: ItemWS1CountGoods):
    url = WS1_URL + 'count'
    try:
        req = requests.post(url=url, data=item.json())
    except requests.exceptions.ConnectionError as e:
        return "WS_1 offline -- try later"
    return req.json()


@app.post("/manage_goods")
def manage_goods_post(data: dict[str, ItemWS2],
                      user: str = Depends(validate_credentials)
):
    url = WS2_URL + 'manage'
    data_json = json.dumps({k: dict(v) for k, v in data.items()})
    print(data_json)
    try:
        req = requests.post(url=url, data=data_json)
    except requests.exceptions.ConnectionError as e:
        return "WS_2 offline -- try later"
    return req.json()


@app.delete("/manage_goods")
def manage_goods_delete(data: dict[int, ItemWS2],
                        user: str = Depends(validate_credentials)
):
    url = WS2_URL + 'manage'
    data_json = json.dumps({k: dict(v) for k, v in data.items()})
    try:
        req = requests.delete(url=url, data=data_json)
    except requests.exceptions.ConnectionError as e:
        return "WS_2 offline -- try later"
    return req.json()
