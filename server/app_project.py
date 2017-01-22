import config
from server.db import session
from server.app_redis import redis
from server.project import Project
from server.data_sources import SqlalchemyData, PandasData

import pandas as pd

if config.data_type == 'csv':
    df = pd.read_csv('~/data/movie-reviews.csv')
    data = PandasData(df, df.columns)
elif config.data_type == 'sql':
    data = SqlalchemyData(config.sql_uri, config.sql_table, config.sql_index)

project = Project(config.project_labels, data, session, redis)

