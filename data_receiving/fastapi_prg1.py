from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(title="My FastAPI API", description="A simple example API", version="1.0.0")

# Data model using Pydantic
class Item(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Name of the item")
    description: Optional[str] = Field(None, max_length=200, description="Description of the item")
    price: float = Field(..., gt=0, description="Price of the item")
    tax: Optional[float] = Field(None, description="Tax applied to the item")

items = {}  # In-memory storage (replace with a database in real applications)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the API!"}

@app.post("/items/", response_model=Item, status_code=201, tags=["Items"])
async def create_item(item: Item):
    if item.name in items:
        raise HTTPException(status_code=400, detail="Item with this name already exists")
    items[item.name] = item
    return item

@app.get("/items/", response_model=List[Item], tags=["Items"])
async def read_items(q: Optional[str] = Query(None, max_length=50, description="Search query")):
    if q:
        filtered_items = [item for item in items.values() if q.lower() in item.name.lower() or (item.description and q.lower() in item.description.lower())]
        return filtered_items
    return list(items.values())

@app.get("/items/{item_name}", response_model=Item, tags=["Items"])
async def read_item(item_name: str):
    if item_name not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_name]

@app.put("/items/{item_name}", response_model=Item, tags=["Items"])
async def update_item(item_name: str, item: Item):
    if item_name not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_name] = item
    return item

@app.delete("/items/{item_name}", tags=["Items"], status_code=204)
async def delete_item(item_name: str):
    if item_name not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_name]
    return None # 204 status code does not return a body


#Run the server
#uvicorn main:app --reload