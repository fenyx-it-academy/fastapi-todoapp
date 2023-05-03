# make necessary imports

from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from uuid import UUID, uuid4
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# create the FastAPI class

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[""],
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=["*"],
)


class Todo(BaseModel):
    id: str
    name: str
    status: Optional[str] = "pending"


todo_lst = [
    Todo(id=str(uuid4()), name="Do homework"),
    Todo(id=str(uuid4()), name="Shopping"),
    Todo(id=str(uuid4()), name="Reading", status="Done"),
]


@app.get("/", include_in_schema=False)
async def read_root():
    # """
    # A landing page displaying a message.
    # """
    # return {"message": "Hello World!"}

    """
    A landing page displaying a message.
    """
    with open("client/main.html", "r") as f:
        index_html = f.read()
    return HTMLResponse(content=index_html, status_code=200)


@app.get("/client/{file_path:path}", include_in_schema=False)
async def serve_static_files(file_path: str):
    """
    Serves static files located in the client/ directory.
    """
    return FileResponse(f"client/{file_path}")


@app.get("/todos")
async def get_todos():
    """
    Returns a list of all todos.
    """
    return todo_lst


@app.get("/todo/{item_id}")
async def get_todo(item_id: str):
    """
    Returns a particular todo item by its id.
    """
    for todo in todo_lst:
        if todo.id == item_id:
            return todo
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/newtodo")
async def create_todo(todo: Todo):
    """
    Creates a new todo item and adds it to the todo list.
    """
    if not todo.id:
        todo.id = str(uuid4())
    todo_lst.append(todo)
    return todo


@app.put("/todoupdate/{item_id}")
async def update_todo_status(item_id: str, status: str):
    """
    Updates the status of a todo item with a given id.
    """
    for todo in todo_lst:
        if todo.id == item_id:
            todo.status = status
            return todo
    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/tododelete/{item_id}")
async def delete_todo_by_id(item_id: str):
    """
    Deletes a todo item with a given id.
    """
    for todo in todo_lst:
        if todo.id == item_id:
            todo_lst.remove(todo)
            return todo_lst
    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/todoclear")
async def delete_all_todos():
    """
    Deletes all todo items from the list.
    """
    todo_lst.clear()
    return todo_lst


# THINGS TO KEEP IN MIND:

# work in specific branches (git checkout -b feature/<feature_name_of_your_branch>)

# make sure to specify each function by creating docstrings, here's an example:
# """Search for a single user
# Args:
#     user_id (UUID): id of the user
# Returns:
#    JSON: JSON representation of user details
# """


# use proper error handling - check FastAPI docs.

# install the following VsCode extensions:
# autoDocstring - Python Docstring Generator
# Live Server


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="ToDo App API",
        version="1.0.0",
        description='This is an API for a todo app by <a href="https://github.com/TheRamy/">TheRamy</a> <br>',
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
