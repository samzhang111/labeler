import config
from server.db import session
from server.project import SqlalchemyData, PandasData, Project

#import pandas as pd
#df = pd.read_csv('~/data/movie-reviews.csv')
#pandas_data = PandasData(df, df.columns)
#project = Project(config.project_labels, pandas_data, session)

sql_data = SqlalchemyData(config.sql_uri, config.sql_table, config.sql_index)
project = Project(config.project_labels, sql_data, session)
