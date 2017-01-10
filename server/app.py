from flask import Flask, request, jsonify, render_template
from server.app_project import project

app = Flask(__name__)

@app.route('/labels')
def get_labels():
    return jsonify({
            'labels': project.labels,
            'columns': project.data_columns
            })

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
    project.assign_labels(post_id, data['labels'])

    return jsonify({'index': post_id})

@app.route('/')
def index():
    return render_template('index.html')

