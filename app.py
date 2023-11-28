from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from dotenv import load_dotenv
import os
from bson import json_util

load_dotenv()
app = Flask(__name__)
CORS(app)
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
mongo = PyMongo(app)

# Define the MongoDB collection
typeit_space_collection = mongo.db.Typeit


@app.route('/create_typeit_space', methods=['POST'])
def create_typeit_space():
    data = request.get_json()
    space_name = data.get('space_name')

    # Insert the TypeIt space into the MongoDB collection
    typeit_space_collection.insert_one({'space_name': space_name, 'comments': []})

    return jsonify({'message': f'TypeIt Space "{space_name}" created successfully'})


@app.route('/list_typeit_spaces', methods=['GET'])
def list_typeit_spaces():
    # Retrieve the list of TypeIt spaces from the MongoDB collection
    typeit_spaces = typeit_space_collection.distinct('space_name')
    return jsonify({'typeit_spaces': typeit_spaces})


@app.route('/list_comments/<space_name>', methods=['GET'])
def list_comments(space_name):
    # Retrieve comments for a specific TypeIt space from the MongoDB collection
    typeit_space = typeit_space_collection.find_one({'space_name': space_name})

    if typeit_space:
        comments = typeit_space['comments']
        return jsonify({'comments': comments})
    else:
        return jsonify({'error': f'TypeIt Space "{space_name}" not found'}), 404


@app.route('/add_to_diary_blog', methods=['POST'])
def add_to_diary_blog():
    data = request.get_json()
    space_name = data.get('space_name')
    comment = data.get('comment')

    # Update comments for the TypeIt space in the MongoDB collection
    result = typeit_space_collection.update_one({'space_name': space_name}, {'$push': {'comments': comment}})

    if result.modified_count > 0:
        return jsonify({'message': 'Comment added successfully'})
    else:
        return jsonify({'error': f'TypeIt Space "{space_name}" not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
