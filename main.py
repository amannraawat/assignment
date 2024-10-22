from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId
from pymongo import MongoClient

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://amannraawat:fakeaccount12345@cluster0.vuzdwqs.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
mongo = PyMongo(app)

client = MongoClient('mongodb+srv://amannraawat:fakeaccount12345@cluster0.vuzdwqs.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

db = client['myUser']
users_collection = db.users

@app.route('/')
def home():
    return "Flask Mongodb app is running"

@app.route('/users', methods=['GET'])
def get_all_users():
    users = users_collection.find()
    result = []
    for user in users:
        result.append({
            'id': str(user['_id']),
            'name': str(user['name']),
            'email': str(user['email']),
            'password': str(user['password'])
        })
    return jsonify(result), 200

@app.route('/users/<id>', methods=['GET'])
def get_specific_user(id):
    user = users_collection.find_one({'_id': ObjectId(id)})
    if user:
        result = {
            'id': str(user['_id']),
            'name': str(user['name']),
            'email': str(user['email']),
            'password': str(user['password'])
        }
        return jsonify(result), 200
    else:
        return jsonify({'error': 'User Not Found.'}), 404
    
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid input, no JSON data received'}), 400
    
    
    if 'name' in data and 'email' in data and 'password' in data:
        user_id = users_collection.insert_one({
            'name': data['name'],
            'email': data['email'],
            'password': data['password']
        }).inserted_id
        return jsonify({'id': str(user_id)}), 201
    else:
        return jsonify({'error': 'Missing required fields'}), 400
    
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid input'}), 400
    
    updated_data = {}
    if 'name' in data:
        updated_data['name'] = data['name']
    if 'email' in data:
        updated_data['email'] = data['email']
    if 'password' in data:
        updated_data['password'] = data['password']
        
    result = users_collection.update_one({'_id': ObjectId(id)}, {'$set': updated_data})
    if result.matched_count > 0:
        return jsonify({'message': 'User updated successfully'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404
    
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    result = users_collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
