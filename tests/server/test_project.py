import unittest
from expects import *
from server.models import Label
from server.project import Project
from collections import defaultdict


class FakeSession(object):
    def __init__(self):
        self.labels = []
        self.commit_called = False

    def add(self, label):
        self.labels.append(label)

    def commit(self):
        self.commit_called = True

class FakeRedis(object):
    def __init__(self, data=defaultdict(set)):
        self.data = data
        self.calls = defaultdict(list)

    def srandmember(self, label):
        self.calls['srandmember'].append(label)
        return next(iter(self.data[label]))

    def scard(self, label):
        return len(self.data[label])

    def srem(self, label, ix):
        self.data[label].discard(ix)


class TestProject(unittest.TestCase):
    def test_can_assign_empty_labels(self):
        fake_session = FakeSession()
        fake_redis = FakeRedis()
        project = Project(labels=[], data=None, session=fake_session, redis=fake_redis)

        project.assign_labels(1, [])

        expect(fake_session.labels).to(equal([Label(document_id=1, label=None)]))

    def test_assigns_all_labels(self):
        fake_session = FakeSession()
        fake_redis = FakeRedis()
        project = Project(labels=[], data=None, session=fake_session, redis=fake_redis)

        test_labels = [500, 900]
        project.assign_labels(1, test_labels)

        expect(fake_session.labels).to(equal([
            Label(document_id=1, label=500),
            Label(document_id=1, label=900),
        ]))

    def test_assigning_label_removes_index_from_redis(self):
        fake_session = FakeSession()
        fake_redis = FakeRedis({'unlabeled': {1}})
        project = Project(labels=[], data=None, session=fake_session, redis=fake_redis)

        test_labels = [500, 900]

        expect(fake_redis.scard('unlabeled')).to(equal(1))
        project.assign_labels(1, test_labels)
        expect(fake_redis.scard('unlabeled')).to(equal(0))


    def test_receives_unlabeled_datum_from_redis_without_deleting(self):
        fake_session = FakeSession()
        fake_redis = FakeRedis({'unlabeled': {1}})
        project = Project(labels=[], data=None, session=fake_session, redis=fake_redis)

        datum = project.get_unlabeled_datum_index()
        expect(datum).to(equal(1))

        datum = project.get_unlabeled_datum_index()
        expect(datum).to(equal(1))

