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

