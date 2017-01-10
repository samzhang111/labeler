from server import project_config
from server.db import session
from server.project import SqlalchemyData, Project

#import pandas as pd
#df = pd.read_csv('~/data/abalone.csv')
#pandas_data = PandasData(df, df.columns)
#project = Project(project_config.project_labels, pandas_data)

sql_data = SqlalchemyData(project_config.sql_uri, project_config.sql_table, project_config.sql_index)
project = Project(project_config.project_labels, sql_data, session)
