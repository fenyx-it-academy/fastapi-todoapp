# make necessary imports

from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import UUID, uuid4
from fastapi.middleware.cors import CORSMiddleware
import uvicorn



# create the FastAPI class
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Todo (BaseModel):
    id: UUID
    name: str
    status: Optional [str] = "pending"


todo_lst=[Todo(id=uuid4(),name='Do homework'),
Todo(id=uuid4(),name='Shopping'),
Todo(id=uuid4(),name='Reading',status='Done')]

@app.get("/")
def read_root():
    return{"Good Luck":"team 2 and 3"}

# create a todo list and add 3 Todo items to serve as examples
@app.post("/add_todos")
def create_todo(todo: Todo):
    new_todo = Todo(id=uuid4(), name=todo.name, status=todo.status)
    todo_lst.append(new_todo)
    return {"message": "Todo created successfully", "todo": new_todo}


# create a get req. listener for the landing page "/"
# return hello world or sth random as a response object
@app.get("/")
def read_root():
    return{"hello":"World"}


# create a get req. listener for the endpoint "/todos"
# return all todos as a response object
@app.get("/todos")
async def get_all_todos():
    return {"todos": todo_lst}


# create a get req. listener for the a single todo item, customize the path using item id
# return the particular item as a response object
@app.get("/get_item_todos/{todo_id}")
def get_todo_id(todo_id:UUID):
    for i in todo_lst:
        if i.id == todo_id:
            return {"todo": i}
    return HTTPException(status_code=404, detail="Todo not found")

# create a post req. listener for creating a new todo item
# return the newly created item as a response object
@app.post("/create_todos")
def crate_todo(item: Todo):
    t = Todo(name = item.name)
    todo_lst.append(t)
    return t


# create a put req. listener for updating an existing todo item
# return the updated item as a response object
@app.put("/updat_todos/{todo_id}")
def update_item(todo_id: UUID, todo: Todo):
    t = None
    for i, j in enumerate(todo_lst):
        if j.id == todo_id:
            t = i
            break

    if t is not None:
        todo_lst[t].name = todo.name
        todo_lst[t].status = todo.status
        return todo_lst[t]
    else:
        raise HTTPException(status_code=404, detail="Todo item not found")

# create a delete req. listener for deleting a todo item
# return the final list of todos as a response object
@app.delete("/Delete_todos/{todo_id}")
def delete_todo_item(todo_id: UUID):
    t = None
    for i, j in enumerate(todo_lst):
        if j.id == todo_id:
            t = i
            break
    if t is not None:
        todo_lst.pop(t)
        return todo_lst
    else:
        raise HTTPException(status_code=404, detail="Todo item not found")


# create a delete req. listener for deleting all todo items
# return the  final list of todos, which would be an empty list, as a response object
@app.delete("delete_all")
def delete_all():
    global todo_lst
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
