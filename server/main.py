# make necessary imports
from typing import Optional
from fastapi import FastAPI , HTTPException
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
    id: Optional [UUID]
    name: str
    status: Optional [str] = "pending"

# create a todo list and add 3 Todo items to serve as examples

todoList=[Todo(id=uuid4(),name='Do homework'),
Todo(id=uuid4(),name='Shopping'),
Todo(id=uuid4(),name='Reading',status='completed')]

# create a get req. listener for the landing page "/"
# return hello world or sth random as a response object

@app.get("/")
def read_root():
    """This is the landing page

    Returns:
        dictionary: Greeting
    """
    return {"Good luck": "team 2 and 3"}

# create a get req. listener for the endpoint "/todos"
# return all todos as a response object
@app.get("/todos")
def read_todos():
    """This function shows all todo list

    Returns:
        list of dectionary: all items in todo list
    """
    return todoList


# create a get req. listener for the a single todo item, customize the path using item id
# return the particular item as a response object
@app.get("/todos/{item_id}")
def read_todo(item_id:UUID):
    """This function shows one todo

    Args:
        item_id (UUID): id of todo item

    Raises:
        HTTPException: This will be raised when the id does not exist in the todo list

    Returns:
        dictionary: one element of todo list
    """
    for i in todoList:
        if i.id == item_id:
            return i
    raise HTTPException(status_code=404, detail="Item does not exist.")
   

# create a post req. listener for creating a new todo item
# return the newly created item as a response object
@app.post("/todos")
def add_item(todo:Todo):
    """This method add a new todo task

    Args:
        todo (Todo): class of Todo

    Returns:
        dictionary: the todo id, name and status
    """
    new_todo = Todo(id=uuid4(), name=todo.name)
    todoList.append(new_todo)
    return new_todo



# create a put req. listener for updating an existing todo item
# return the updated item as a response object
@app.put("/todos-update/{id}")
def update_todos(todo_update:Todo,id:UUID):
    """This function updates a todo item

    Args:
        todo_update (Todo): todo item
        id (UUID): todo id

    Raises:
        HTTPException: will be raised in case the todo doesn't exist

    Returns:
        dictionary: the updated todo item
    """
    for i in todoList:
        if i.id == id:
            if todo_update.name is not None:
                i.name = todo_update.name
            if todo_update.status is not None:
                i.status = todo_update.status
            return todoList
    raise HTTPException(status_code=404, detail= f"This todo doesn't exist")


@app.put("/todos/{id}")
def update_todos(id:UUID):
    """This method updates the status of a todo item

    Args:
        id (UUID): todo item id description

    Raises:
        HTTPException: will be raised in case the todo item doesn't exist

    Returns:
        list of dictionaries: All todo items after updateing one of the todo item status
    """
    for i in todoList:
        if i.id == id:
            if i.status == 'pending':
                i.status = 'completed'
            else:
                i.status = 'pending'
            return todoList
    raise HTTPException(status_code=404, detail= f"This todo doesn't exist")



# create a delete req. listener for deleting a todo item
# return the final list of todos as a response object
@app.delete("/todos/{id}")
def delete_todo(id:UUID):
    """This method deletes one todo item

    Args:
        id (UUID): todo item id

    Raises:
        HTTPException: this will be raised when the todo item doesn't exist

    Returns:
        list of dictionaries: all todo items after deleting the item that it's id was passed
    """
    for i in todoList:
        if i.id == id:
            todoList.remove(i)
            print("item found")
            return todoList
    raise HTTPException(status_code=404, detail= f"This todo doesn't exist")



# create a delete req. listener for deleting all todo items
# return the  final list of todos, which would be an empty list, as a response object
@app.delete("/todos")
def delete_todo():
    """This function delets all items in the todo list

    Returns:
        list: empty list
    """
    todoList.clear()
    return todoList





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
