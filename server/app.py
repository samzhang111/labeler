from flask import Flask, request, jsonify, render_template
from server.app_project import project

app = Flask(__name__)

from functools import wraps
from flask import request, Response
import os

from server.db import init_db
init_db()

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    actual_username = os.getenv('FLASK_USER', None)
    actual_password = os.getenv('FLASK_PASSWORD', None)


    if not actual_username or not actual_password:
        return True

    return username == actual_username and password == actual_password

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/labels')
def get_labels():
    return(jsonify({
        'labels': project.labels,
        'columns': project.data_columns
        }))

@app.route('/unlabeled')
def get_unlabeled():
    ix = project.get_unlabeled_datum_index()
    return jsonify({'index': ix})

@app.route('/data/<int:index>')
def get_datum(index):
    return jsonify(project.datum(index))

@app.route('/data/<int:post_id>/label', methods=['POST'])
def post_label(post_id):
    data = request.get_json(force=True)
    project.assign_labels(post_id, data['labels'], data['userId'],
            request.remote_addr)

    return jsonify({'index': post_id})

@app.route('/user/<string:user>')
def get_user(user):
    completed = project.get_completed(user)

    return jsonify({'completed': completed})

@app.route('/')
@requires_auth
def index():
    return render_template('index.html')

