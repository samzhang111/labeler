from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

class Project(object):
    def __init__(self, labels, data):
        self.labels = [{'value': i, 'text': label} for i, label in enumerate(labels)]
        self.data = data
        self.unlabeled = set(data.index)
        self.labeled_data = dict()

    def assign_labels(self, datum_id, labels):
        self.unlabeled.remove(datum_id)
        self.labeled_data[datum_id] = labels

    def get_unlabeled_datum_index(self):
        ix = next(iter(self.unlabeled))
        return ix.item()

    def datum(self, ix):
        return self.data.iloc[ix]

    @property
    def data_columns(self):
        return list(self.data.columns)

project = Project(['Spam', 'Not spam'], pd.read_csv('~/data/abalone.csv'))

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
    return project.datum(index).to_json()

@app.route('/data/<int:post_id>/label', methods=['POST'])
def post_label(post_id):
    data = request.get_json(force=True)
    project.assign_labels(post_id, data['labels'])

    return jsonify({'index': post_id})

@app.route('/')
def index():
    return render_template('index.html')

