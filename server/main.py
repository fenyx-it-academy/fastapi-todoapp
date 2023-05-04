# make necessary imports
from typing import Optional
from fastapi import FastAPI,HTTPException
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






# create a todo list and add 3 Todo items to serve as examples
todo_lst=[Todo(id=uuid4(),name='Do homework'),
Todo(id=uuid4(),name='Shopping'),
Todo(id=uuid4(),name='Reading',status='Done')]


# create a get req. listener for the landing page "/"
# return hello world or sth random as a response object
@app.get("/")
def read_root():
    return {"Hello World!"}


# create a get req. listener for the endpoint "/todos"
# return all todos as a response object
@app.get("/todos")
def return_all_todos():
    return todo_lst


# create a get req. listener for the a single todo item, customize the path using item id
# return the particular item as a response object
@app.get("/single-todo")
def retrun_todo(id: str):
    for s_todo in todo_lst:
        if str(s_todo.id) == id:
            return s_todo
    raise HTTPException(status_code=404, detail= "Item Not Found! Please try again ")


# create a post req. listener for creating a new todo item
# return the newly created item as a response object
@app.post("/create-todo")
def create_todo(todo:Todo):
    todo_item = Todo(name = todo.name)
    todo_lst.append(todo_item)
    return todo_item


# create a put req. listener for updating an existing todo item
# return the updated item as a response object
@app.put("/update-todo")
def update_todo(todo: Todo): 
    for item in todo_lst:
        if item.id == todo.id:
            if todo.name != "":
                item.name = todo.name
            if todo.status != "":
                item.status = todo.status
            return item
    raise HTTPException(status_code=404, detail="Item Not Found!")


# create a delete req. listener for deleting a todo item
# return the final list of todos as a response object
@app.delete("/delete-todo/{id}")
def delete_item(id: str):
    for index, item in enumerate(todo_lst):
        if str(item.id) == id:
            del todo_lst[index]
            return todo_lst
    raise HTTPException(status_code=404, detail="Item not found.")


# create a delete req. listener for deleting all todo items
# return the  final list of todos, which would be an empty list, as a response object
@app.delete("/delete-all")
def delete_all_todos():
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
