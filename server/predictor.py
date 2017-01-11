from sklearn.linear_model import SGDClassifier
from sklearn.exceptions import NotFittedError

class OnlinePredictor(SGDClassifier):
    def predict_proba(self, data):
        try:
            return super(OnlinePredictor, self).predict_proba(data)
        except NotFittedError:
            return 0
