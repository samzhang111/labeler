from server.db import Base
from sqlalchemy import Column, Integer, String, func, literal_column

class Label(Base):
    __tablename__ = 'labels'
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer)
    label = Column(Integer)
    labeler = Column(String)
    labeler_ip = Column(String)

    def __init__(self, document_id, label, labeler, ip):
        self.document_id = document_id
        self.label = label
        self.labeler = labeler
        self.labeler_ip = ip

    def __repr__(self):
        return '<Label {} | {}: {} | by {} at {}>'.format(self.id, self.document_id, self.label, self.labeler, self.labeler_ip)

    def __eq__(self, other):
        return self.document_id == other.document_id and self.label == other.label

    @classmethod
    def get_completed(cls, session, user):
        return session.query(cls.labeler).group_by(cls.document_id).having(cls.labeler == user).count()

    @classmethod
    def label_counts(cls, session):
        return session.query(cls.label, func.count(cls.id)).group_by(cls.label).all()

    @classmethod
    def labelset_counts(cls, session):
        inner_table = session.query(
                func.group_concat(cls.label, ',').label('labelset'),
                func.count(cls.id).label('count')
                ).group_by(cls.labeler, cls.document_id).subquery()

        return session.query(
                inner_table.columns.labelset,
                func.sum(inner_table.columns.count)
                ).group_by('labelset').all()

    @classmethod
    def total(cls, session):
        return session.query(func.count(cls.id)).scalar()

    @classmethod
    def total_docs(cls, session):
        return session.query(func.count(func.distinct(cls.document_id))).scalar()

    @classmethod
    def user_counts(cls, session):
        return session.query(cls.labeler, func.count(func.distinct(cls.document_id))).group_by(cls.labeler).all()

