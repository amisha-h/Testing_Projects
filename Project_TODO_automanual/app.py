from flask import Flask, request, jsonify, abort

app = Flask(__name__)


tasks = []
task_id_counter = 1


@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    data = request.get_json()
    if not data or 'title' not in data:
        abort(400, description="Title is required")
    task = {
        'id': task_id_counter,
        'title': data['title'],
        'description': data.get('description', ''),
        'status': 'pending'
    }
    tasks.append(task)
    task_id_counter += 1
    return jsonify(task), 201

# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks), 200

# Get a task by id
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        abort(404, description="Task not found")
    return jsonify(task), 200

# Update a task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        abort(404, description="Task not found")
    if not data:
        abort(400, description="Request body is required")
    task['title'] = data.get('title', task['title'])
    task['description'] = data.get('description', task['description'])
    task['status'] = data.get('status', task['status'])
    return jsonify(task), 200

# Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({'message': 'Task deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
