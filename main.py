from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    name: str
    description: str


items = {}
item_id_counter = 1


# GET запрос: Получение всех элементов
@app.get("/items/")
def read_items():
    return items


# GET запрос: Получение элемента по ID
@app.get("/items/{item_id}")
def read_item(item_id: int):
    item = items.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# POST запрос: Создание нового элемента
@app.post("/items/")
def create_item(item: Item):
    global item_id_counter
    item_id = item_id_counter
    item_id_counter += 1
    items[item_id] = item
    return {"item_id": item_id}


# PUT запрос: Обновление элемента по ID
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = item
    return {"item_id": item_id, }


# DELETE запрос: Удаление элемента по ID
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    return {"message": f"Item {item_id} has been deleted"}


# PATCH запрос: Частичное обновление элемента по ID
@app.patch("/items/{item_id}")
def update_item_partial(item_id: int, item_update: Item):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    current_item = items[item_id]
    update_data = item_update
    updated_item = current_item.copy(update=update_data)
    items[item_id] = updated_item
    return {"message": f"Item {item_id} has been updated", "updated_item": updated_item}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
