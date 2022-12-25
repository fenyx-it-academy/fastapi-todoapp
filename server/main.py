# make necessary imports


# create the FastAPI class


# add CORS middleware




# creata a Todo class by inheriting BaseModel from Pydantic lib.
# attributes to be included:
    # - id: Optional UUID
    # - name: str
    # - status: Optional str default_val= "pending"


# create a todo list and add 3 Todo items to serve as examples



# create a get req. listener for the landing page "/"
# return hello world or sth random as a response object



# create a get req. listener for the endpoint "/todos"
# return all todos as a response object



# create a get req. listener for the a single todo item, customize the path using item id
# return the particular item as a response object



# create a post req. listener for creating a new todo item
# return the newly created item as a response object



# create a put req. listener for updating an existing todo item
# return the updated item as a response object



# create a delete req. listener for deleting a todo item
# return the final list of todos as a response object



# create a delete req. listener for deleting all todo items
# return the  final list of todos, which would be an empty list, as a response object






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