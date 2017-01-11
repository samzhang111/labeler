import config
from server.db import session
from server.project import SqlalchemyData, PandasData, Project
from server.predictor import OnlinePredictor
from sklearn.feature_extraction.text import HashingVectorizer

predictors = []
for label in config.project_labels:
    predictors.append(OnlinePredictor(loss='log', average=True))

vectorizer = HashingVectorizer(n_features = 2**18, non_negative=True)

import pandas as pd
df = pd.read_csv('~/data/text.csv')
pandas_data = PandasData(df, df.columns)
project = Project(config.project_labels, pandas_data, session, config.text_column, predictors, vectorizer)

#sql_data = SqlalchemyData(config.sql_uri, config.sql_table, config.sql_index)
#project = Project(config.project_labels, sql_data, session)
