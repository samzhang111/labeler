import pandas as pd
from server.db import session
from server.models import Label
from server import project_config
import json


class Project(object):
    def __init__(self, labels, data):
        self.labels = [{'value': i, 'text': label} for i, label in enumerate(labels)]
        self.data = data
        all_indexes = set(data.index)
        labeled_indexes = set([x[0] for x in session.query(Label.id).all()])

        self.unlabeled = all_indexes - labeled_indexes

    def assign_labels(self, datum_id, labels):
        self.unlabeled.remove(datum_id)
        label = Label(datum_id, labels)
        session.add(label)
        session.commit()

    def get_unlabeled_datum_index(self):
        ix = next(iter(self.unlabeled))
        return ix

    def datum(self, ix):
        return self.data[ix]

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

    @property
    def index(self):
        return [int(x) for x in self.dataframe.index]


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
        result = self.session.query(self.table).filter_by(**{self.index_column: index}).first()._asdict()

        return result

    @property
    def index(self):
        return [getattr(row, self.index_column) for row in self.session.query(self.table)]


#df = pd.read_csv('~/data/abalone.csv')
#pandas_data = PandasData(df, df.columns)
sql_data = SqlalchemyData(project_config.sql_uri, project_config.sql_table, project_config.sql_index)
project = Project(project_config.project_labels, sql_data)
