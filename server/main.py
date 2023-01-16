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
    id: UUID
    name: str
    status: Optional [str] = "pending"

class UpdateTodo(BaseModel):
    id: Optional[UUID] 
    name: Optional[str] 
    status: Optional[str] 


# create a todo list and add 3 Todo items to serve as examples

todo_list=[Todo(id=uuid4(),name='Do homework'),
Todo(id=uuid4(),name='Shopping'),
Todo(id=uuid4(),name='Reading',status='Done')]

# create a get req. listener for the landing page "/"
# return hello world or sth random as a response object

@app.get("/")
def read_root():
    return {"Good luck": "team 2 and 3"}

# create a get req. listener for the endpoint "/todos"
# return all todos as a response object

@app.get("/todos")
def read_todos():
    return todo_list


# create a get req. listener for the a single todo item, customize the path using item id
# return the particular item as a response object
@app.get("/todos/{item_id}")
def read_todo(item_id:UUID):
    for i in todo_list:
        if i.id == item_id:
            return i
    raise HTTPException(status_code=404, detail="Item name is not found.")
   

# create a post req. listener for creating a new todo item
# return the newly created item as a response object
@app.post("/add-item")
def add_item(todo: Todo):
    if todo in todo_list:
        return {"Error":"item alredy exists."}
    
    todo_list.append(todo)
    return todo




# create a put req. listener for updating an existing todo item
# return the updated item as a response object
@app.put("/update-item/{item_id}")
def update_item(item_id:UUID, item:UpdateTodo):
    for i, todo in enumerate(todo_list):
        if todo.id == item_id:
            if item.name != None:
                todo_list[i].name = item.name
            if item.status != None:
                todo_list[i].status = item.status
            return todo_list[i]
    raise HTTPException(status_code=404, detail="Item not found.")



# create a delete req. listener for deleting a todo item
# return the final list of todos as a response object
@app.delete("/todos/{item_id}")
def delete_item(item_id:UUID):
    for item in todo_list:
        if item.id == item_id:
            todo_list.remove(item)
    return todo_list



# create a delete req. listener for deleting all todo items
# return the  final list of todos, which would be an empty list, as a response object
@app.delete("/todos/clearlist")
def delete_all():
    todo_list.clear()
    return todo_list

@app.delete("/todos/clearlist")
def delete_all():
    del todo_list[:]
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
