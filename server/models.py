from server.db import Base
from sqlalchemy import Column, Integer, String

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
