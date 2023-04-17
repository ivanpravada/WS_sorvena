from db import MyDatabase
from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException

app = FastAPI()


@app.post("/manage")
def manage_post(data: dict):
    with MyDatabase() as db:
        goods_in_db = [i[0] for i in db.select('select title from goods')]
    user_goods = [i['title'] for i in data.values()]

    if set(user_goods).issubset(goods_in_db):
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail="It is not possible to add existing products")

    set_to_add = set(user_goods).difference(goods_in_db)
    list_to_add = []
    for key, value in data.items():
        if value['title'] in set_to_add:
            list_to_add.append((data[key]['title'], data[key]['price']))

    query = f"insert into goods (title, price) values {str(list_to_add).strip('[]')};"
    with MyDatabase() as db:
        db.insert(query)
        res = db.select('select * from goods')
    res_dict = {i[0]: {'title': i[1], 'price': i[2]} for i in res}
    return res_dict


@app.delete("/manage")
def manage_delete(data: dict):
    with MyDatabase() as db:
        goods_in_db = [i[0] for i in db.select('select title from goods')]
    user_goods = [i['title'] for i in data.values()]

    if not set(goods_in_db).intersection(user_goods):
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail="It is not possible to delete existing products")

    set_to_delete = set(user_goods).intersection(goods_in_db)
    list_to_delete = []
    for key, value in data.items():
        if value['title'] in set_to_delete:
            list_to_delete.append(data[key]['title'])

    query = f"delete from goods where title in ({str(list_to_delete).strip('[]')});"
    with MyDatabase() as db:
        db.delete(query)
        res = db.select('select * from goods')
    res_dict = {i[0]: {'title': i[1], 'price': i[2]} for i in res}
    return res_dict
