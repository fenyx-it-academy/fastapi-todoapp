from fastapi import FastAPI
from pydantic import BaseModel
import uuid
from typing import Optional
import uvicorn

class Todo(BaseModel):
    id: Optional[uuid.UUID]
    name: str
    status: Optional[str] = "pending"

# create Todo class by inheriting from BaseModel
class Todo(BaseModel):
    id: Optional[uuid.UUID]
    name: str
    status: Optional[str] = "pending"

# create a todo list and add 3 Todo items to serve as examples
todo_list = [
    Todo(id=uuid.uuid4(), name="Take out the trash"),
    Todo(id=uuid.uuid4(), name="Buy groceries"),
    Todo(id=uuid.uuid4(), name="Do laundry")
]

app = FastAPI()

# create a get req. listener for the landing page "/"
# return hello world or sth random as a response object
@app.get("/")
def read_root():
    return {"Hello": "Semih"}

# create a get req. listener for the endpoint "/todos"
# return all todos as a response object
@app.get("/todos")
def read_todos():
    return todo_list

# create a get req. listener for the a single todo item, customize the path using item id
# return the particular item as a response object
@app.get("/todos/{todo_id}")
def read_todo(todo_id: uuid.UUID):
    for todo in todo_list:
        if todo.id == todo_id:
            return todo
    return {"error": "Todo not found"}

# create a post req. listener for creating a new todo item
# return the newly created item as a response object
@app.post("/todos")
def create_todo(todo: Todo):
    todo_list.append(todo)
    return todo

# create a put req. listener for updating an existing todo item
# return the updated item as a response object
@app.put("/todos/{todo_id}")
def update_todo(todo_id: uuid.UUID, todo: Todo):
    for i, existing_todo in enumerate(todo_list):
        if existing_todo.id == todo_id:
            todo_list[i] = todo
            return todo
    return {"error": "Todo not found"}

# create a delete req. listener for deleting a todo item
# return the final list of todos as a response object
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: uuid.UUID):
    for i, existing_todo in enumerate(todo_list):
        if existing_todo.id == todo_id:
            del todo_list[i]
            return todo_list
    return {"error": "Todo not found"}

# create a delete req. listener for deleting all todo items
# return the final list of todos, which would be an empty list, as a response object
@app.delete("/todos")
def delete_all_todos():
    todo_list.clear()
    return todo_list

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)