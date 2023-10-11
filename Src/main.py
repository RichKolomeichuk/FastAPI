from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str


items = {}


class ItemMixin:
    items = items


class GetMixin(ItemMixin):
    @classmethod
    def read_items(cls):
        return cls.items

    @classmethod
    def read_item(cls, item_id: int):
        item = cls.items.get(item_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item


@app.get("/items/")
def read_items():
    return GetMixin.read_items()


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return GetMixin.read_item(item_id)


class PostMixin(ItemMixin):
    @classmethod
    def create_item(cls, item: Item):
        item_id = len(cls.items) + 1
        cls.items[item_id] = item
        return {"item_id": item_id, }


@app.post("/items/")
def create_item(item: Item):
    return PostMixin.create_item(item)


class PutMixin(ItemMixin):
    @classmethod
    def update_item(cls, item_id: int, item: Item):
        if item_id not in cls.items:
            raise HTTPException(status_code=404, detail="Item not found")
        cls.items[item_id] = item
        return {"item_id": item_id, }


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return PutMixin.update_item(item_id, item)


class DeleteMixin(ItemMixin):
    @classmethod
    def delete_item(cls, item_id: int):
        if item_id not in cls.items:
            raise HTTPException(status_code=404, detail="Item not found")
        del cls.items[item_id]
        return {"message": f"Item {item_id} has been deleted"}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return DeleteMixin.delete_item(item_id)


class PatchMixin(ItemMixin):
    @classmethod
    def update_item_partial(cls, item_id: int, item_update: Item):
        if item_id not in cls.items:
            raise HTTPException(status_code=404, detail="Item not found")
        current_item = cls.items[item_id]
        update_data = item_update
        updated_item = current_item.copy(update=update_data)
        cls.items[item_id] = updated_item
        return {"message": f"Item {item_id} has been updated", "updated_item": updated_item}


@app.patch("/items/{item_id}")
def update_item_partial(item_id: int, item_update: Item):
    return PatchMixin.update_item_partial(item_id, item_update)
