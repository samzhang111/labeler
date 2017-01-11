import sys
from ..app_redis import redis
from ..app_project import project

def load_unlabeled_into_redis():
    ids = project.get_unlabeled_set(10)
    for id in ids:
        redis.sadd('unlabeled', id)

