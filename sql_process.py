from sqlalchemy import Table, select
from sqlalchemy.dialects.postgresql import insert
import pandas as pd


def get_dict(tbl_name, metadata, engine, con):
    """
    Get the index dictionary from SQL database.

    Parameters:
        tbl_name (str): Name of the table in SQL database.
        metadata (sqlalchemy.sql.schema.MetaData): SQL database metadata.
        engine (sqlalchemy.engine.Engine): SQL database engine.
        con (sqlalchemy.engine.base.Connection): Connection to SQL database server.

    Returns:
        dic (dict)
    """
    dic = {}

    tbl = Table(tbl_name, metadata, autoload=True, autoload_with=engine)
    df = pd.read_sql(select([tbl]), con)

    for i, row in df.iterrows():
        dic[row['answer']] = row['id']

    return dic


def sheet2sql(db_tbl, con, row, tbl_dict):
    """
    Transfer data from Google Sheet to SQL database.

    Parameters:
        db_tbl (sqlalchemy.sql.schema.Table): SQLAlchemy Table object.
        con (sqlalchemy.engine.base.Connection): Connection to SQL database server.
        row(dict): Row to insert presented in format of dictionary.
        tbl_dict(dict): Index dictionary of a table.

    Returns:
        None
    """

    kwargs_dict = {}
    for k, v in tbl_dict.items():
        kwargs_dict[k] = v[1].get(row.get(v[0]))

    stmt = insert(db_tbl).values(**kwargs_dict)
    con.execute(stmt)
