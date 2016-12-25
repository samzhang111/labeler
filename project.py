import pandas as pd

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
