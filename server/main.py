# make necessary imports
from typing import Optional
from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from uuid import UUID, uuid4
from fastapi.middleware.cors import CORSMiddleware
import uvicorn



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TodoItem(BaseModel):
    id: Optional[UUID]
    name: str
    status: Optional[str] = "pending"




todo_list=[TodoItem(id=uuid4(),name='Do homework'),
TodoItem(id=uuid4(),name='Shopping'),
TodoItem(id=uuid4(),name='Reading', status='Done')]




@app.get("/")
def read_root():
    return {'Welcome TodoApp'}
    """_summary_

    Root:
       "/"

    Returns:
        Welcome TodoApp
    """
    

@app.get("/todos")
def read_todos():
    return todo_list
    """_summary_

    Root:
        "/todos"

    Returns:
       all todos as a response object
    """
    

@app.get("/todos/{item_id}")
def read_todo(item_id:UUID):
    for todo in todo_list:
        if todo.id == item_id:
            return todo
    raise HTTPException(status_code=404, detail="Item name is not found.")
    """_summary_

    Root:
        "/todos/{item_id}"
    Returns:
        the particular item as a response object
    """
   


@app.post("/todos")
def create_todo(item: TodoItem):
    todo_list.append(item) 
    return todo_list
    """_summary_

    Post reguest: 
       create a new todo item

    Returns:
        the newly created item as a response object
    """
        


@app.put("/todos")
def update_todo( item: TodoItem):
    for todo in todo_list:
        if todo.id == item.id:
            todo.status = item.status
            return todo
    raise HTTPException(status_code=404, detail="Item does not exists.")
    """_summary_

    Put request:
        update an existing todo item

    Returns:
        the updated item as a response object
    """

                                

@app.delete("/todos/{item_id}")
def delete_todo(item_id: UUID):
    for i, todo in enumerate(todo_list):
        if todo.id == item_id:
            todo_list.pop(i)
            return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item does not exists.")
    """_summary_
    Delete request:
        delete todo item


    Returns:
        the final list of todos as a response object
    """
    


@app.delete("/todos")
def delete_all_todos():
    todo_list.clear()
    return todo_list
    """_summary_
      delete request:  
        delete all list


    Returns:
        an empty list
    """



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
