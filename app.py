from flask import Flask, request, jsonify
from flask import Response
from flask_pymongo import PyMongo
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import ReturnDocument
from bson import json_util
import bcrypt
import jwt
import os


load_dotenv()
app = Flask(__name__)
CORS(app)
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
mongo = PyMongo(app)
secret_key = os.environ.get('SECRET_KEY')

typeit_spaces = {}
diary_blog = {}


@app.route('/create_typeit_space', methods=['POST'])
def create_typeit_space():
    data = request.get_json()
    space_name = data.get('space_name')
    typeit_spaces[space_name] = {'comments': []}
    return jsonify({'message': f'TypeIt Space "{space_name}" created successfully'})


# Step 3: See list of TypeIt Spaces
@app.route('/list_typeit_spaces', methods=['GET'])
def list_typeit_spaces():
    return jsonify({'typeit_spaces': list(typeit_spaces.keys())})


# Step 4: See list of comments in a TypeIt Space
@app.route('/list_comments/<space_name>', methods=['GET'])
def list_comments(space_name):
    if space_name in typeit_spaces:
        comments = typeit_spaces[space_name]['comments']
        return jsonify({'comments': comments})
    else:
        return jsonify({'error': f'TypeIt Space "{space_name}" not found'}), 404


# Step 5: Add TypeIt component into DiaryBlog
@app.route('/add_to_diary_blog', methods=['POST'])
def add_to_diary_blog():
    data = request.get_json()
    space_name = data.get('space_name')
    comment = data.get('comment')

    if space_name in typeit_spaces:
        typeit_spaces[space_name]['comments'].append(comment)

        # Optionally, you may want to add the comment to the DiaryBlog
        diary_blog.setdefault(space_name, []).append(comment)

        return jsonify({'message': 'Comment added successfully'})
    else:
        return jsonify({'error': f'TypeIt Space "{space_name}" not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
