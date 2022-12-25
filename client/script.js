// getting all required elements
const inputBox = document.querySelector(".inputField input");
const addBtn = document.querySelector(".inputField button");

window.onload = renderAllTodos;

async function fetchTodos() {
  const response = await fetch('http://127.0.0.1:8000/todos');
  const todos = await response.json();
  return todos;
}

function renderAllTodos() {
  fetchTodos().then(todoList => {
    const todoDiv = document.querySelector(".todoList");
    todoDiv.innerHTML = '';
    todoList.forEach(renderTodo);

    const pendingTasksNumb = document.querySelector(".pendingTasks");
    const pluralTask = document.querySelector(".pluralTask");
    pendingTasksNumb.textContent = todoList.length; //passing the array length in pendingtask
    
    if (todoList.length > 0) {
      clearAllButton.classList.add("active");
    } else {
      clearAllButton.classList.remove("active");
    }

    if (todoList.length == 1) {
      pluralTask.textContent ='';
    } else {
      pluralTask.textContent = 's'; 
    }

  });
}


function renderTodo(todo) {
  const todoList = document.querySelector(".todoList");
  // Create a new list item
  const newTodoItem = document.createElement('li');
  newTodoItem.innerHTML = `
    <input type="checkbox" ${todo.status === 'completed' ? 'checked' : ''} >
    ${todo.name}
    <span class="icon-del"><i class="fas fa-trash"></i></span>
  `;
  newTodoItem.id = `todo-${todo.id}`;
  newTodoItem.style.textDecoration = todo.status === "completed" ? 'line-through' : 'none';

  // Add the new list item to the todo list
  todoList.appendChild(newTodoItem);

  // Add an event listener for the checkbox
  const checkbox = newTodoItem.querySelector('input[type="checkbox"]');
  checkbox.addEventListener('change', () => {
    // Get the current status of the todo item
    const todoItem = document.getElementById(`todo-${todo.id}`);
    const checkbox = todoItem.querySelector('input[type="checkbox"]');
    const status = checkbox.checked ? 'completed' : 'pending';
    // Update the todo item's status on the server
    updateTodoStatus(todo.id, status);
  });

  // Add an event listener for the delete button
  const deleteButton = newTodoItem.querySelector('.icon-del');
  deleteButton.addEventListener('click', () => {
    deleteTodo(todo.id);
  });
}



function updateTodoStatus(id, status) {
  console.log(id, status)
  fetch(`http://127.0.0.1:8000/todos`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      "id": id,
      "status": status,
      "name": ""
    })
  })
    .then(response => {
      // If the update request was successful, update the todo item's status on the page
      if (response.ok) {
        const todoItem = document.getElementById(`todo-${id}`);
        const checkbox = todoItem.querySelector('input[type="checkbox"]');
        checkbox.checked = status === 'completed';
        todoItem.style.textDecoration = checkbox.checked ? 'line-through' : 'none';
      } else {
        // Otherwise, display an error message
        alert('An error occurred while trying to update the todo item');
      }
    })
    .catch(error => {
      // Display an error message if there was an issue with the request
      alert('An error occurred while trying to update the todo item');
    });
}


const clearAllButton = document.querySelector(".footer button");
clearAllButton.onclick = () => {
   // Send the DELETE request to the server
   fetch('http://127.0.0.1:8000/todos', { method: 'DELETE' })
   .then(response => {
     // If the delete request was successful, remove all the todo items from the page
     if (response.ok) {
       const todoList = document.querySelector(".todoList");
       todoList.innerHTML = '';
     } else {
       // Otherwise, display an error message
       alert('An error occurred while trying to delete all the todo items');
     }
   })
   .catch(error => {
     console.log(error)
     // Display an error message if there was an issue with the request
     alert('An error occurred while trying to delete all the todo items');
   });
 renderAllTodos();
}

// onkeyup event activate add button
inputBox.onkeyup = () => {
  let userEnteredValue = inputBox.value; //getting user entered value
  if (userEnteredValue.trim() != 0) { //if the user value isn't only spaces
    addBtn.classList.add("active"); //activate the add button
  } else {
    addBtn.classList.remove("active"); //deactivate the add button
  }
}


// send new item request
addBtn.onclick = () => { //when user click on plus icon button
  let userEnteredValue = inputBox.value; //getting input field value
  addItem(userEnteredValue);
  addBtn.classList.remove("active"); //deactivate the add button once the task added
  inputBox.value = ""; //once task added leave the input field blank
}


function deleteTodo(id) {
  // Send the DELETE request to the server
  fetch(`http://127.0.0.1:8000/todos/${id}`, {
    method: 'DELETE'
  })
    .then(response => {
      // If the delete request was successful, remove the todo item from the page
      if (response.ok) {
        const todoItem = document.getElementById(`todo-${id}`);
        todoItem.parentNode.removeChild(todoItem);
      } else {
        // Otherwise, display an error message
        alert('An error occurred while trying to delete the todo item');
      }
    })
    .catch(error => {
      // Display an error message if there was an issue with the request
      console.log(error);
    });
    // renderAllTodos();
}


function addItem(val) {
  fetch(`http://127.0.0.1:8000/todos`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      "name": val
    })
  })
    .then(res => {
      if (res.ok) {
        return res.json();
      } else {
        throw new Error(res.statusText);
      }
    })
    .then(data => {
      console.log(data)
    })
    .catch(error => {
      console.log(error)
    })
  renderAllTodos();
}


