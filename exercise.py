import json
import os.path
from typing import Annotated
from fastapi import FastAPI , Form
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

#
# cars = []
# next_id = 1
#
#
# class CarForm(BaseModel):
#     name: str
#     price: float
#
# class SearchFrom(BaseModel):
#     name: str
#
# class DeleteForm(BaseModel):
#     name: str
#
# @app.get("/cars" , tags=['Template'])
# async def search_page(request: Request):
#     return templates.TemplateResponse(request, name='cars_list.html')
# @app.post("/cars", tags=['Template'])
# async def search_car(data: Annotated[SearchFrom, Form()]):
#     if data.name:
#         result = [c for c in cars if data.name.lower() in c["name"].lower()]
#         if not result:
#             return JSONResponse(content={"message": "Mashina topilmadi"}, status_code=404)
#         return result
#     return cars
#
#
# # ---- Add----
#
# @app.get("/cars/add", tags=['Template'])
# async def add_page(request: Request):
#     return templates.TemplateResponse(request, name="cars_add.html")
#
#
# @app.post("/cars/add", tags=['Template'])
# async def add_cars(data: Annotated[CarForm, Form()]):
#     global next_id
#     cars.append({"id": next_id, "name": data.name, "price": data.price})
#     next_id += 1
#     return JSONResponse(content={"message": f"{data.name} qoshildi"}, status_code=201)
#
# # ----delete----
#
# @app.get("/cars/delete", tags=['Template'])
# async def delete_page(request: Request):
#     return templates.TemplateResponse(request, name="cars_delete.html")
#
# @app.post("/cars/delete", tags=['Template'])
# async def delete_cars(data:Annotated[DeleteForm, Form()]):
#     for car in cars:
#         if car["id"] == id:
#             cars.remove(car)
#             return {"message": f"{car['name']} ochirildi"}
#     return JSONResponse(content={"message": "Mashina topilmadi"}, status_code=404)

DB_FILE = "todos.json"

def load_todos():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
def save_todos(todos):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=4)

class TodoForm(BaseModel):
    title: str

class SearchForm(BaseModel):
    title: str

class DeleteForm(BaseModel):
    id: int

class UpdateForm(BaseModel):
    id: int
    title: str | None = None
    completed: bool | None = None


@app.get("/todos", tags=['Template'])
async def todos_page(request: Request):
    todos = load_todos()

    return templates.TemplateResponse(request, name='todos_list.html', context={"todos": todos})


# ----- List and Search -----
@app.post("/todos/search", tags=['Template'])
async def search_todo(data: Annotated[SearchForm, Form()]):
    todos = load_todos()

    if data.title:
        result = [t for t in todos if data.title.lower() in t["title"].lower()]
        if not result:
            return JSONResponse(content={"message": "Vazifa topilmadi"}, status_code=404)
        return result
    return todos

# ----- ADD -----
@app.get("/todos/add", tags=['Template'])
async def add_page(request: Request):
    return templates.TemplateResponse(request, name="todos_add.html")


@app.post("/todos/add", tags=['Template'])
async def add_todo(data: Annotated[TodoForm, Form()]):
    todos = load_todos()
    next_id = max([t["id"] for t in todos], default=0) + 1
    new_todo = {"id": next_id,"title": data.title,"completed": False}
    todos.append(new_todo)
    save_todos(todos)
    return JSONResponse(content={"message": f"'{data.title}' qoshildi"}, status_code=201)


# ---- Delete ----

@app.get("/todos/delete", tags=['Template'])
async def delete_page(request: Request):
    return templates.TemplateResponse(request, name="todos_delete.html")

@app.post("/todos/delete", tags=['Template'])
async def delete_todo(data: Annotated[DeleteForm, Form()]):
    todos = load_todos()
    for todo in todos:
        if todo["id"] == data.id:
            todos.remove(todo)
            save_todos(todos)
            return {"message": f"ID: {data.id} - vazifa ochirildi"}
    return JSONResponse(content={"message": "Vazifa topilmadi"}, status_code=404)


# ----- Update -----

@app.get("/todos/update", tags=['Template'])
async def update_page(request: Request):
    return templates.TemplateResponse(request, name="todos_update.html")

@app.post("/todos/update", tags=['Template'])
async def update_todo(data: Annotated[UpdateForm, Form()]):
    todos = load_todos()

    for todo in todos:
        if todo["id"] == data.id:
            if data.title is not None and data.title.strip() != "":
                todo["title"] = data.title

            if data.completed is not None:
                todo["completed"] = data.completed

            save_todos(todos)
            return {"message": f"ID: {data.id} - vazifa yangilandi", "todo": todo}

    return JSONResponse(content={"message": "Vazifa topilmadi"}, status_code=404)









