# make necessary imports
from typing import Optional
from fastapi import FastAPI
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

class UpdateTodo (BaseModel):
    id: Optional [UUID]
    name: Optional [str]
    status: Optional [str] 

# create a todo list and add 3 Todo items to serve as examples
todo_lst=[
Todo(id=uuid4(),name='Do homework'),
Todo(id=uuid4(),name='Shopping'),
Todo(id=uuid4(),name='Reading',status='Done')
]

# create a get req. listener for the landing page "/"
# return hello world or sth random as a response object
@app.get("/")
def read_root():
    return {"what about": "to do something?"}


# create a get req. listener for the endpoint "/todos"
# return all todos as a response object
@app.get("/todos")
def all_todo():
    return todo_lst

# create a get req. listener for the a single todo item, customize the path using item id
# return the particular item as a response object

@app.get("/todo/{item_id}")
def get_todo(item_id:UUID):
    for i in todo_lst:
        if i.id == item_id:
            return i
    raise HTTPException(status_code=404, detail="Item name is not found.")



# create a post req. listener for creating a new todo item
# return the newly created item as a response object

@app.post("/create-todo")
def create_todo(todo:Todo):
    if id in todo_lst:
        return {"Error":"This ID already exists."}
    
    todo_lst.append(todo)
    return todo

# create a put req. listener for updating an existing todo item
# return the updated item as a response object
@app.put("/put-todo/{item_id}")
def update_todo(item_id:UUID,todo:UpdateTodo):
    if todo.id == item_id:
        if todo.name != None:
            todo_lst[item_id].name = todo.name
        if todo.status != None:
            todo_lst[item_id].status = todo.status
    return todo_lst[item_id]
    
    
    # for i, todo in enumerate (todo_lst):
    #     if todo.id == item_id:
    #         if todo.name != None:
    #             todo_lst[i].name = todo.name
    #         if todo.status != None:
    #             todo_lst[i].status = todo.status
    #         return todo_lst[i]
    # raise HTTPException(status_code=404, detail="Item not found.")



# create a delete req. listener for deleting a todo item
# return the final list of todos as a response object
@app.delete("/delite/{item_id}")
def del_todo(item_id:UUID):
    for item in todo_lst:
        if item.id == item_id:
            todo_lst.remove(item)
    return todo_lst




# create a delete req. listener for deleting all todo items
# return the  final list of todos, which would be an empty list, as a response object
@app.delete("/delite/all")
def del_all_todo():
    # todo_lst.clear()
    # return todo_lst
    # global todo_lst
    # todo_lst = []
    del todo_lst[:]
    return {"message": "List cleared"}
    







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
