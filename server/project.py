import pandas as pd
from server.models import Label
from server.app_redis import unlabeled
import json


class Project(object):
    def __init__(self, labels, data, session, redis):
        self.labels = [{'value': i, 'text': label} for i, label in enumerate(labels)]
        self.data = data
        self.session = session
        self.redis = redis

    def assign_labels(self, datum_id, labels, labeler, ip):
        self.redis.srem(unlabeled, datum_id)
        if not labels:
            label = Label(document_id=datum_id, label=None, labeler=labeler, ip=ip)
            self.session.add(label)

        for label in labels:
            label = Label(document_id=datum_id, label=int(label),
                    labeler=labeler, ip=ip)
            self.session.add(label)

        self.session.commit()

    def get_unlabeled_datum_index(self):
        return int(self.redis.srandmember(unlabeled))

    def datum(self, ix):
        return self.data[ix]

    @property
    def data_columns(self):
        return list(self.data.columns)

    @property
    def labeled_indexes(self):
        return set([x[0] for x in self.session.query(Label.document_id).distinct().all()])

    def get_unlabeled_set(self, n):
        return self.data.get_unlabeled_set(self.labeled_indexes, n)


class PandasData(object):
    def __init__(self, dataframe, columns):
        self.dataframe = dataframe
        self.columns = columns

    def __getitem__(self, index):
        jsons = self.dataframe.iloc[index].to_json()
        return json.loads(jsons)

    def get_unlabeled_set(self, labeled_indexes, n):
        unlabeled = set()
        for ix in self.dataframe.index:
            if ix not in labeled_indexes:
                unlabeled.add(ix.item())
                if len(unlabeled) >= n:
                    return unlabeled
        return unlabeled

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

    def get_unlabeled_set(self, labeled_indexes, n):
        unlabeled_set = set()
        result = self.session.query(self.table).filter(~getattr(self.table.c, self.index_column).in_(labeled_indexes)).limit(n).all()
        for row in result:
            unlabeled_set.add(getattr(row, self.index_column))
        return unlabeled_set

