from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# In-memory storage for simplicity
items = {}

class Item(BaseModel):
    name: str
    age: int
    gender: str
    mobile_no: str

@app.post("/items/", response_model=Item)
def create_item(item: Item):
    if item.name in items:
        raise HTTPException(status_code=400, detail="Item already exists")
    items[item.name] = item
    return item

@app.get("/items/", response_model=List[Item])
def read_items():
    return list(items.values())

@app.get("/items/{item_name}", response_model=Item)
def read_item(item_name: str):
    if item_name not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_name]

@app.put("/items/{item_name}", response_model=Item)
def edit_item(item_name: str, item: Item):
    if item_name not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_name] = item
    return item

@app.delete("/items/{item_name}")
def delete_item(item_name: str):
    if item_name not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_name]
    return {"detail": "Item deleted"}
