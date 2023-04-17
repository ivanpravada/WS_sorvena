import json
from db import MyDatabase
from fastapi import FastAPI, Request, status
from pydantic import BaseModel
from fastapi.exceptions import HTTPException

app = FastAPI()


class ItemWS1CountGoods(BaseModel):
    title: str
    count: int


@app.get("/goods")
def goods(product: Request):
    db = MyDatabase()
    client_query = product.url.query

    if not client_query:
        res = db.select('select * from goods')
    else:
        list_query = tuple([i.split('=')[-1] for i in client_query.split('&')])
        if len(list_query) == 1:
            list_query = f"('{list_query[0]}')"
        res = db.select(f'select * from goods where title in {list_query}')
    res_dict = {i[0]: {'title': i[1], 'price': i[2]} for i in res}
    db.close()
    return res_dict


@app.post("/count")
def count(item: ItemWS1CountGoods):
    client_goods = json.loads(item.json())
    title = client_goods["title"]
    db = MyDatabase()
    res = db.select(f"select * from goods where title = '{title}'")
    if res:
        res_dict = {
            str(res[0][0]): {
                'title': res[0][1],
                'price': res[0][2],
                'count': client_goods["count"],
                'sum': client_goods["count"] * res[0][2]
            }
        }
        db.close()
        return res_dict
    db.close()
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="The operation cannot be performed")
