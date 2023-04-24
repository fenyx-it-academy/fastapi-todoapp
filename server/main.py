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
    return {"Hello":"World"}

# create a get req. listener for the endpoint "/todos"
# return all todos as a response object
@app.get("/todos")
def all_todos():
    """displays all the todos list
    Args:
         no argument
    Returns:
        List: list of all todo dictionaries
    """
    return todo_lst


# create a get req. listener for the a single todo item, customize the path using item id
# return the particular item as a response object
@app.get("/single-todo")
def single_todo(id:str):
    """search for a single to do

    Args:
        id (str): id of the todo item

    Raises:
        HTTPException: rises an error if the todo id is not in the list.

    Returns:
        dictionary: a single todo with its id, name and status.
    """
    for items in todo_lst:
        if str(items.id) == id:
           return items
    raise HTTPException(status_code=404, detail="Item not found.")

# create a post req. listener for creating a new todo item
# return the newly created item as a response object

@app.post("/new-todo")
def new_todo(todo:Todo):
    """ add a new todo in to a list

    Args:
        dictionary: a single todo with its id, name and status.

    Raises:
        HTTPException: raises an error if the todo id is already in use.

    Returns:
        dictionary: the newly added todo with its id, name and status.
    """
    for items in todo_lst:
        if items.id == todo.id:
          raise HTTPException(status_code=412, detail="Item_id is occupid try another.")
    todo_lst.append(todo)
    return todo

# create a put req. listener for updating an existing todo item
# return the updated item as a response object
@app.put("/update-todo")
def update_todo(todo: Todo):
    """updates one of the todos in the list

    Args:
        dictionary: a single todo with its id, name and status.

    Raises:
        HTTPException: rises an error if the todo id is not in the list.

    Returns:
         dictionary: the newly added todo with its id, name and status.
    """
    for items in todo_lst:
        if items.id == todo.id:
            if todo.name != "":
                items.name = todo.name
            if todo.status != "":
                items.status = todo.status
            return items
    raise HTTPException(status_code=404, detail="Item not found.")


# create a delete req. listener for deleting a todo item
# return the final list of todos as a response object

@app.delete("/delete-todo")
def delete_todo(id: str):
    """deletes a single todo 

    Args:
        id (str): id of the todo item

    Raises:
        HTTPException: rises an error if the todo id is not in the list.

    Returns:
        List: list of remained todo dictionaries
    """
    for items in todo_lst:
        if str(items.id) == id: 
          todo_lst.remove(items)
          return todo_lst
    raise HTTPException(status_code=404, detail="Item not found.")

# create a delete req. listener for deleting all todo items
# return the  final list of todos, which would be an empty list, as a response object
@app.delete("/delete-all")
def delete_all():
    """deletes all todos in a list 

    Returns:
        List: empty list
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
