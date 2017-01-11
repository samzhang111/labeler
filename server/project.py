import pandas as pd
from server.models import Label
import json


class Project(object):
    def __init__(self, labels, data, session, text_column, predictors, vectorizer):
        self.labels = [{'value': i, 'text': label} for i, label in enumerate(labels)]
        self.data = data
        self.session = session

        self.text_column = text_column
        self.predictors = predictors
        self.vectorizer = vectorizer

    def assign_labels(self, datum_id, labels):
        if not labels:
            label = Label(document_id=datum_id, label=None)
            self.session.add(label)

        for label in labels:
            label = Label(document_id=datum_id, label=int(label))
            self.session.add(label)

        self.session.commit()

    def get_unlabeled_datum_index(self):
        labeled_indexes = set([x[0] for x in self.session.query(Label.document_id).distinct().all()])
        return self.data.get_unlabeled(labeled_indexes)

    def datum(self, ix):
        return self.data[ix]

    def predict(self, datum):
        X = self.vectorizer.transform([datum[self.text_column]])
        predictions = {}
        for i, predictor in enumerate(self.predictors):
            predictions[i] = predictor.predict_proba(X)

        return predictions

    def train(self, datum, labels):
        print('Received labels: ', labels)
        X = self.vectorizer.transform([datum[self.text_column]])
        for i, predictor in enumerate(self.predictors):
            if str(i) in labels:
                print('Labeling {} as true'.format(self.labels[i]['text']))
                predictor.partial_fit(X, [1], classes=[0, 1])
            else:
                print('Labeling {} as false'.format(self.labels[i]['text']))
                predictor.partial_fit(X, [0], classes=[0, 1])

    @property
    def data_columns(self):
        return list(self.data.columns)


class PandasData(object):
    def __init__(self, dataframe, columns):
        self.dataframe = dataframe
        self.columns = columns

    def __getitem__(self, index):
        jsons = self.dataframe.iloc[index].to_json()
        return json.loads(jsons)

    def get_unlabeled(self, labeled_indexes):
        for ix in self.dataframe.index:
            if ix not in labeled_indexes:
                return ix.item()


from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
class SqlalchemyData(object):
    def __init__(self, uri, table, index_column):
        self.engine = create_engine(uri, convert_unicode=True)
        self.session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))

        self.table = table
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)
        self.table = self.metadata.tables[table]
        self.index_column = index_column
        self.columns = [c.name for c in self.table.columns]

    def __getitem__(self, index):
        result = self.session.query(self.table).filter(getattr(self.table.c, self.index_column) == index).first()._asdict()

        return result

    def get_unlabeled(self, labeled_indexes):
        result = self.session.query(self.table).filter(~getattr(self.table.c, self.index_column).in_(labeled_indexes)).first()
        return getattr(result, self.index_column)


