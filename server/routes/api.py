from flask import request, jsonify, Blueprint
from server.app_project import project

api = Blueprint('api', __name__)

@api.route('/labels')
def get_labels():
    return(jsonify({
        'labels': project.labels,
        'columns': project.data_columns
        }))

@api.route('/unlabeled')
def get_unlabeled():
    ix = project.get_unlabeled_datum_index()
    return jsonify({'index': ix})

@api.route('/data/<int:index>')
def get_datum(index):
    return jsonify(project.datum(index))

@api.route('/data/<int:post_id>/label', methods=['POST'])
def post_label(post_id):
    data = request.get_json(force=True)
    project.assign_labels(post_id, data['labels'], data['userId'],
            request.remote_addr)

    return jsonify({'index': post_id})

@api.route('/user/<string:user>')
def get_user(user):
    completed = project.get_completed(user)

    return jsonify({'completed': completed})

@api.route('/summary')
def summary():
    return jsonify(project.get_summary())
