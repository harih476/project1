
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    description: str

items_db = []

@app.post("/items/", response_model=Item)
def create_item(item: Item):
    for existing_item in items_db:
        if existing_item.id == item.id:
            raise HTTPException(status_code=400, detail="Item with this ID already exists.")
    items_db.append(item)
    return item

@app.get("/items/", response_model=List[Item])
def get_items():
    return items_db

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found.")

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for idx, item in enumerate(items_db):
        if item.id == item_id:
            items_db[idx] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found.")

@app.delete("/items/{item_id}", response_model=dict)
def delete_item(item_id: int):
    for idx, item in enumerate(items_db):
        if item.id == item_id:
            del items_db[idx]
            return {"message": "Item deleted successfully."}
    raise HTTPException(status_code=404, detail="Item not found.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
