from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Sample data to act as our database
todos = []
next_id = 1

# Endpoint to retrieve all to-do items
@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify({"todos": todos})

# Endpoint to retrieve a single to-do item by ID
@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = next((todo for todo in todos if todo["id"] == todo_id), None)
    if todo is None:
        abort(404, description="To-do item not found")
    return jsonify(todo)

# Endpoint to create a new to-do item
@app.route('/todos', methods=['POST'])
def create_todo():
    global next_id
    if not request.json or 'title' not in request.json:
        abort(400, description="Missing 'title' in request data")

    todo = {
        "id": next_id,
        "title": request.json['title'],
        "description": request.json.get('description', ''),
        "completed": request.json.get('completed', False)
    }
    todos.append(todo)
    next_id += 1
    return jsonify(todo), 201

# Endpoint to update an existing to-do item by ID
@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = next((todo for todo in todos if todo["id"] == todo_id), None)
    if todo is None:
        abort(404, description="To-do item not found")

    if not request.json:
        abort(400, description="Request data must be in JSON format")
    
    # Update fields if they are in the request JSON
    todo['title'] = request.json.get('title', todo['title'])
    todo['description'] = request.json.get('description', todo['description'])
    todo['completed'] = request.json.get('completed', todo['completed'])
    
    return jsonify(todo)

# Endpoint to delete a to-do item by ID
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todo = next((todo for todo in todos if todo["id"] == todo_id), None)
    if todo is None:
        abort(404, description="To-do item not found")
    
    todos = [todo for todo in todos if todo["id"] != todo_id]
    return jsonify({"result": True})

if __name__ == '__main__':
    app.run(debug=True)