from server.db import Base
from sqlalchemy import Column, Integer

class Label(Base):
    __tablename__ = 'labels'
    id = Column(Integer, primary_key=True)
    label = Column(Integer)

    def __init__(self, id, label):
        self.id = id
        self.label = label

    def __repr__(self):
        return '<Label {}: {}>'.format(self.id, self.label)
