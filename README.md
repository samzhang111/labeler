#Text Labeler

A tool to help label texts with truth data. 

It takes a pandas dataframe or a SQL database as an input, as well as a list of truth labels. Then it shows the user one record from the data at a time, allowing them to choose one of the labels. It saves the result into a sqlite database.

##Inputs
The data to be labeled should be defined in `config.py`. See `config.py.template` for the necessary variables.

##Outputs
The labels will be saved in a sqlite table in the home directory called `labels.sqlite`.

License: GPL v3
