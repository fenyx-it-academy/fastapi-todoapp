# make necessary imports
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
    id: int
    name: str
    status: Optional [str] = "pendingTasks"

# create a todo list and add 3 Todo items to serve as examples

todoList=[Todo(id=1,name='Do homework'),
Todo(id=2,name='Shopping'),
Todo(id=3,name='Reading',status='Done')]


@app.get("/")
def read_root():
    return {"Hello": "world!"}



@app.get("/todos")
def read_todos():
    return todoList


@app.get("/todos/{item_id}")
def read_todo(item_id:int):
    for i in todoList:
        if i.id == item_id:
            return i
    raise HTTPException(status_code=404, detail="Item name is not found.")
   

@app.post("/new-todos")
def post_item(item:Todo):
   
        newTodoItem=Todo(**{"id":item.id, "name":item.name,"status":item.status })
        todoList.append(newTodoItem)
        return newTodoItem 
    # todo_list.append(new_todo)



@app.put("/update-todo-byId/{todo_id}")
def update_item(todo_id:int,item:Todo):
    
   
    for todo in todoList:
        if todo_id !=todo.id:
            raise HTTPException(status_code=500,detail="todo_id is not found") 
        else: 
            todoList.remove(todo)
            updated_todo=todo(**{"id":item.id, "name":item.name,"status":item.status })
            todoList.append(updated_todo)
            return updated_todo
        
    

@app.delete("/delete/{todo_id}")
def delete_item(todo_id:int):
    
    
    for todo in todoList:
        
        if todo_id != todo.id:
            raise HTTPException(status_code=500,detail="the item is not found")
        else:
            todoList.remove(todo)
            return todoList
            
        

@app.delete("/delete-all-todos")
def delete():
    if todoList==[]:
        raise HTTPException(status_code=500,detail="there is no item")
    else:
        del todoList[:]
        return todoList
    

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)






