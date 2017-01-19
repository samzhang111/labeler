from flask import Flask, request, jsonify, render_template
from server.app_project import project

app = Flask(__name__)

from functools import wraps
from flask import request, Response
import os

from server.db import init_db
init_db()


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
def index():
    return render_template('index.html')

