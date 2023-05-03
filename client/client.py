import typer
import requests
import json
from uuid import UUID, uuid4
from typing import Optional

app = typer.Typer()

BASE_URL = "http://localhost:8000"

class Todo:
    def __init__(self, id: UUID, name: str, status: Optional[str] = "pending"):
        self.id = id
        self.name = name
        self.status = status

    def __repr__(self):
        return f"{self.name} ({self.id}): {self.status}"

@app.command()
def show_all():
    """
    Display all todo items
    """
    response = requests.get(f"{BASE_URL}/todos")
    if response.ok:
        todos_data = json.loads(response.text)
        todos = [Todo(**item) for item in todos_data]
        if len(todos) == 0:
            typer.echo("No todo items yet!")
        else:
            for todo in todos:
                typer.echo(todo)
    else:
        typer.echo(f"Error: {response.status_code} - {response.text}")

@app.command()
def add_todo(name: str):
    """
    Add a new todo item with the given name
    """
    new_todo = Todo(id=str(uuid4()), name=name)
    response = requests.post(f"{BASE_URL}/newtodo",
                             data=json.dumps(new_todo.__dict__),
                             headers={"Content-Type": "application/json"})
    if response.ok:
        todo_data = json.loads(response.text)
        todo = Todo(**todo_data)
        typer.echo(f"Added new todo: {todo}")
    else:
        typer.echo(f"Error: {response.status_code} - {response.text}")

@app.command()
def update_todo_status(item_id: str, status: str):
    """
    Updates the status of a todo item with the given id.
    """
    response = requests.put(f"{BASE_URL}/todoupdate/{item_id}?status={status}")
    if response.ok:
        todo_data = json.loads(response.text)
        todo = Todo(**todo_data)
        typer.echo(f"Updated todo status: {todo}")
    else:
        typer.echo(f"Error: {response.status_code} - {response.text}")

@app.command()
def delete_todo_by_id(item_id: str):
    """
    Deletes a todo item with the given id.
    """
    response = requests.delete(f"{BASE_URL}/tododelete/{item_id}")
    if response.ok:
        todos_data = json.loads(response.text)
        todos = [Todo(**item) for item in todos_data]
        typer.echo(f"Deleted todo with id {item_id}")
        if len(todos) == 0:
            typer.echo("No todo items left!")
        else:
            for todo in todos:
                typer.echo(todo)
    else:
        typer.echo(f"Error: {response.status_code} - {response.text}")

@app.command()
def clear_all():
    """
    Deletes all todo items
    """
    response = requests.delete(f"{BASE_URL}/todoclear")
    if response.ok:
        todos_data = json.loads(response.text)
        todos = [Todo(**item) for item in todos_data]
        typer.echo("Cleared all todo items!")
    else:
        typer.echo(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    app()