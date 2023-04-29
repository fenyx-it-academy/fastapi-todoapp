# make necessary imports
from typing import Optional
from fastapi import FastAPI
from fastapi import HTTPException
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

class New_item (BaseModel):
    name: str

# create a todo list and add 3 Todo items to serve as examples
todo_lst=[Todo(id=uuid4(),name='Do homework'),
Todo(id=uuid4(),name='Shopping'),
Todo(id=uuid4(),name='Reading',status='Done'),
Todo(id=uuid4(),name='Running')]


# create a get req. listener for the landing page "/"
# return hello world or sth random as a response object
@app.get("/")
async def read_root():
    return {"Hello World"}


# create a get req. listener for the endpoint "/todos"
# return all todos as a response object
@app.get("/todos")
def get_todos():
    return list(todo_lst)


# create a get req. listener for the a single todo item, customize the path using item id
# return the particular item as a response object
@app.get("/todos/{item_id}")
async def get_item(item_id: UUID):
    item = [it for it in todo_lst if it.id == item_id][0]
    return item


# create a post req. listener for creating a new todo item
# return the newly created item as a response object
@app.post('/todos')
async def create_item(new_item: New_item):
    # if name is None:
    #     raise HTTPException(status_code=404, detail="Todo Item with this name not found")
    
    item = Todo(id = uuid4(), name = new_item.name)
    todo_lst.append(item)
    return todo_lst

# create a put req. listener for updating an existing todo item
# return the updated item as a response object
@app.put('/todos')
async def update_status(updated_item: Todo):
    item = [it for it in todo_lst if it.id == updated_item.id][0]
    item.status = updated_item.status
    return item


# create a delete req. listener for deleting a todo item
# return the final list of todos as a response object
@app.delete('/todos/{id}')
async def delete_item(id: UUID):
    item = [it for it in todo_lst if it.id == id][0]
    todo_lst.remove(item)
    return todo_lst

# create a delete req. listener for deleting all todo items
# return the  final list of todos, which would be an empty list, as a response object
@app.delete('/todos')
async def clear_list():
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
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
