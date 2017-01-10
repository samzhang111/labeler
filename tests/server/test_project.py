import unittest
from expects import *
from server.models import Label
from server.project import Project


class FakeSession(object):
    def __init__(self):
        self.labels = []
        self.commit_called = False

    def add(self, label):
        self.labels.append(label)

    def commit(self):
        self.commit_called = True


class TestProject(unittest.TestCase):
    def test_can_assign_empty_labels(self):
        fake_session = FakeSession()
        project = Project(labels=[], data=None, session=fake_session)

        project.assign_labels(1, [])

        expect(fake_session.labels).to(equal([Label(document_id=1, label=None)]))

    def test_assigns_all_labels(self):
        fake_session = FakeSession()
        project = Project(labels=[], data=None, session=fake_session)

        test_labels = [500, 900]
        project.assign_labels(1, test_labels)

        expect(fake_session.labels).to(equal([
            Label(document_id=1, label=500),
            Label(document_id=1, label=900),
        ]))

