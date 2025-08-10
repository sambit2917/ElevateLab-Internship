from flask import Flask,request,jsonify

app = Flask(__name__)

users = [
    {"id": 1, "name": "Sambit", "email": "sambit@gmail.com"},
    {"id": 2, "name": "Chinu", "email": "moharanachinmaya@gmail.com"},
    {"id": 3, "name": "Pradeep", "email": "pradeepkumargupta2002@gmail.com"},
    {"id": 4, "name": "Subha", "email": "shrutisubha@gmail.com"},
    {"id": 5, "name": "John", "email": "john@gmail.com"}
]

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# GET one user by ID
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    for user in users:
        if user['id'] == user_id:
            return jsonify(user)
    return jsonify({'error':'user not found'}),404

# POST - Add new user
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = {
        'id':users[-1]['id']+1 if users else 1,
        'name':data['name'],
        'email':data['email']
    }
    users.append(new_user)
    return jsonify(new_user), 201

# PUT - Update user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    for user in users:
        if user['id'] == user_id:
            user['name'] = data.get('name', user['name'])
            user['email'] = data.get('email', user['email'])
            return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

# DELETE - Remove user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    for user in users:
        if user['id'] == user_id:
            users.remove(user)
            return jsonify({'message': 'User deleted'})
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)