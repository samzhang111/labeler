from server.db import Base
from sqlalchemy import Column, Integer, String

class Label(Base):
    __tablename__ = 'labels'
    id = Column(Integer, primary_key=True)
    labels = Column(String)

    def __init__(self, id, labels):
        self.id = id
        self.labels = ",".join(map(str, labels))

    def __repr__(self):
        return '<Label {}: {}>'.format(self.id, self.label)
