import pandas as pd
from sqlalchemy import create_engine, Table, MetaData, select
from dotenv import load_dotenv
import os

# self-created class and functions
from sql_process import get_dict, sheet2sql
from gsheet_access import Sheet

# load environmental variables
load_dotenv()
TOKEN = os.getenv('TOKEN')
DB_PATH = os.getenv('DB_PATH')

# create engine and connection to SQL database
engine = create_engine(DB_PATH)
con = engine.connect()
metadata = MetaData()

# get an index dictionary
tbl_dict = {'taken_statistics_course': ['Have you ever taken a course in statistics?'],
            'previous_programming_experience': ['Do you have any previous experience with programming?'],
            'why_interested': ['What\'s your interest in data science?'],
            'cats_or_dogs': ['Just for fun, do you prefer dogs or cat?']}
for tbl in tbl_dict:
    tbl_dict[tbl].append(get_dict(tbl, metadata, engine, con))

# create Table object of "responses" table in SQL database
resp_db = Table('responses', metadata, autoload=True, autoload_with=engine)

# create a Sheet object
resp_sheet = Sheet(TOKEN, 'Sample Survey (Responses)', 'Form Responses 1')

# # check dataframe if preprocessing is needed
resp_df = resp_sheet.df
print(resp_df)

# transfer data from Google Sheet to SQL database
for row in resp_sheet.all_values:
    sheet2sql(resp_db, con, row, tbl_dict)

# clear the Google Sheet (except header) to avoid inputting same data again
resp_sheet.clear()

# read the SQL database by converting the table into dataframe
df_from_db = pd.read_sql(select([resp_db]), con, index_col='id')
print(df_from_db)

# close connection to SQL database
con.close()
