// getting all required elements
const inputBox = document.querySelector(".inputField input");
const addBtn = document.querySelector(".inputField button");

window.onload = renderAllTodos;

function fetchTodos() {
  return fetch("http://localhost:8000/todos").then((response) => {
    if (response.ok) {
      return response.json();
    } else {
      throw new Error(response.statusText);
    }
  });
}

function renderAllTodos() {
  fetchTodos().then((todoList) => {
    const todoDiv = document.querySelector(".todoList");
    todoDiv.innerHTML = "";

    todoList.forEach(renderTodo);

    const pendingTasksNumb = document.querySelector(".pendingTasks");
    const pluralTask = document.querySelector(".pluralTask");
    pendingTasksNumb.textContent = todoList.length;
    pluralTask.textContent = todoList.length == 1 ? "" : "s";
    const clearAllButton = document.querySelector(".footer button");
    if (todoList.length > 0) {
      clearAllButton.classList.add("active");
      clearAllButton.onclick = () => {
        deleteAllTodos();
      };
    } else {
      clearAllButton.classList.remove("active");
    }
  });
}

function renderTodo(todo) {
  const todoList = document.querySelector(".todoList");

  const newTodoItem = document.createElement("li");
  newTodoItem.innerHTML = `
    <input type="checkbox" ${todo.status === "completed" ? "checked" : ""}>
    ${todo.name}
    <span class="icon-del"><i class="fas fa-trash"></i></span>
  `;
  newTodoItem.id = `todo-${todo.id}`;
  newTodoItem.style.textDecoration =
    todo.status === "completed" ? "line-through" : "none";

  todoList.appendChild(newTodoItem);

  const checkbox = newTodoItem.querySelector('input[type="checkbox"]');
  checkbox.addEventListener("change", () => {
    const status = checkbox.checked ? "completed" : "pending";
    updateTodoStatus(todo.id, status);
  });

  const deleteButton = newTodoItem.querySelector(".icon-del");
  deleteButton.addEventListener("click", () => {
    deleteTodoItem(todo.id);
  });
}
function updateTodoStatus(todoId, todoStatus) {
  fetch(`http://localhost:8000/todoupdate/${todoId}?status=${todoStatus}`, {
    method: "PUT",
  })
    .then((response) => {
      if (response.ok) {
        const todoItem = document.getElementById(`todo-${todoId}`);
        const checkbox = todoItem.querySelector('input[type="checkbox"]');
        checkbox.checked = todoStatus === "completed";
        todoItem.style.textDecoration = checkbox.checked
          ? "line-through"
          : "none";
      } else {
        throw new Error(
          "An error occurred while trying to update the todo item"
        );
      }
    })
    .catch((error) => {
      alert(error.message);
    });
}

function deleteAllTodos() {
  fetch("http://localhost:8000/todoclear", {
    method: "DELETE",
  })
    .then((response) => {
      if (response.ok) {
        const todoList = document.querySelector(".todoList");
        todoList.innerHTML = "";
        const pendingTasksNumb = document.querySelector(".pendingTasks");
        pendingTasksNumb.textContent = "0";
        const pluralTask = document.querySelector(".pluralTask");
        pluralTask.textContent = "";

        const clearAllButton = document.querySelector(".footer button");
        clearAllButton.classList.remove("active");
      } else {
        throw new Error(
          "An error occurred while trying to delete all the todo items"
        );
      }
    })
    .catch((error) => {
      alert(error.message);
    });
}

function deleteTodoItem(todoId) {
  fetch(`http://localhost:8000/tododelete/${todoId}`, {
    method: "DELETE",
  })
    .then((response) => {
      if (response.ok) {
        const todoItem = document.getElementById(`todo-${todoId}`);
        todoItem.remove();

        const pendingTasksNumb = document.querySelector(".pendingTasks");
        const todoList = document.querySelectorAll(".todoList li");
        pendingTasksNumb.textContent = todoList.length;
        const pluralTask = document.querySelector(".pluralTask");
        pluralTask.textContent = todoList.length == 1 ? "" : "s";

        const clearAllButton = document.querySelector(".footer button");
        if (todoList.length > 0) {
          clearAllButton.classList.add("active");
          clearAllButton.onclick = () => {
            deleteAllTodos();
          };
        } else {
          clearAllButton.classList.remove("active");
        }
      } else {
        throw new Error(
          "An error occurred while trying to delete the todo item"
        );
      }
    })
    .catch((error) => {
      alert(error.message);
    });
}

addBtn.addEventListener("click", () => {
  const inputValue = inputBox.value;
  if (inputValue.trim() !== "") {
    createNewTodoItem(inputValue);
  }
});

inputBox.addEventListener("keyup", (event) => {
  if (event.keyCode === 13) {
    const inputValue = inputBox.value.trim();
    if (inputValue !== "") {
      createNewTodoItem(inputValue);
    }
  }
});


function uuidv4() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

function createNewTodoItem(todoName) {
  fetch("http://localhost:8000/newtodo", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ "id":uuidv4(), "name": todoName }),      
  })
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error(
          "An error occurred while trying to create a new todo item"
        );
      }
    })
    .then((todo) => {
      renderTodo(todo);

      const pendingTasksNumb = document.querySelector(".pendingTasks");
      const todoList = document.querySelectorAll(".todoList li");
      pendingTasksNumb.textContent = todoList.length;
      const pluralTask = document.querySelector(".pluralTask");
      pluralTask.textContent = todoList.length == 1 ? "" : "s";

      const clearAllButton = document.querySelector(".footer button");
      clearAllButton.classList.add("active");
      clearAllButton.onclick = () => {
        deleteAllTodos();
      };
    })
    .catch((error) => {
      alert(error.message);
    });

  inputBox.value = "";
}
