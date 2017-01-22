import pandas as pd
from server.models import Label
from server.app_redis import unlabeled
import json
from sqlalchemy import func


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

    def get_completed(self, user):
        return Label.get_completed(self,session, user)

    def get_summary(self):
        counts = Label.label_counts(self.session)
        labelset_counts = Label.labelset_counts(self.session)
        user_counts = Label.user_counts(self.session)

        counts_with_names = []
        labelset_counts_with_names = []

        for row in counts:
            label_ix = row[0]
            count = row[1]
            if label_ix is None:
                name = 'Skipped'
            else:
                try:
                    name = self.labels[label_ix]['text']
                except IndexError:
                    name = 'Out of range: {}'.format(label_ix)

            counts_with_names.append((name, count))

        for row in labelset_counts:
            count = row[1]

            if row[0] is None:
                name = 'Skipped'
            else:
                label_ix = [int(x) for x in row[0].split(',')]

                try:
                    name = ','.join([self.labels[ix]['text'] for ix in label_ix])
                except IndexError:
                    name = 'Out of range: {}'.format(label_ix)

            labelset_counts_with_names.append((name, count))

        return {
                'counts': counts_with_names,
                'labelset_counts': labelset_counts_with_names,
                'total': Label.total(self.session),
                'total_docs': Label.total_docs(self.session),
                'user_counts': user_counts
                }

