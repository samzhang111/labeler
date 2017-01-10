from server.db import Base
from sqlalchemy import Column, Integer, String

class Label(Base):
    __tablename__ = 'labels'
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer)
    label = Column(Integer)

    def __init__(self, document_id, label):
        self.document_id = document_id
        self.label = label

    def __repr__(self):
        return '<Label {} / {}: {}>'.format(self.id, self.document_id, self.label)
