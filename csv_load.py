
# Import required libraries
import sqlite3
import pandas as pd
  
# Connect to SQLite database
sqlite_file = 'germantown_ten.db'
con = sqlite3.connect(sqlite_file)
  
# Load CSV data into table for each table to be made then Write the data to a sqlite table
nodes_data = pd.read_csv('nodes.csv')
nodes_data.to_sql('nodes', con, if_exists='replace', index=False)
nodes_tags_data = pd.read_csv('nodes_tags.csv')
nodes_tags_data.to_sql('nodes_tags', con, if_exists='replace', index=False)
ways_data = pd.read_csv('ways.csv')
ways_data.to_sql('ways', con, if_exists='replace', index=False)
ways_nodes_data = pd.read_csv('ways_nodes.csv')
ways_nodes_data.to_sql('ways_nodes', con, if_exists='replace', index=False)
ways_tags_data = pd.read_csv('ways_tags.csv')
ways_tags_data.to_sql('ways_tags', con, if_exists='replace', index=False)
  

# Close connection to SQLite database
con.close()
