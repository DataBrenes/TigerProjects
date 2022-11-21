# DuckDB

This is a new database backend that is supposed to be fast and work well with streamlit.  
https://duckdb.org/
https://motherduck.com/
https://shell.duckdb.org/
https://github.com/duckdb/duckdb/blob/master/examples/python/duckdb-python.py # super helpful

You can query dataframes as sequal and interact with them as if tables.  

## Installation 
### Python 
```
pip install duckdb==0.6.0
```
## How to execute SQL queries
First connect to a database using the connect command. By default an in-memory database will be opened.
```
import duckdb
con = duckdb.connect()
```
After connecting, SQL queries can be executed using the execute command.
```
results = con.execute("SELECT 42").fetchall()
```
By default, a list of Python objects is returned. Use df if you would like the result to be returned as a Python dataframe instead.  
```
results = con.execute("SELECT 42").df()
```

## Jupyter notebooks
DuckDB’s Python client can be used directly in Jupyter notebooks with no additional configuration if desired. However, additional libraries can be used to simplify SQL query development. This guide will describe how to utilize those additional libraries. See other guides in the Python section for how to use DuckDB and Python together.  

As a small note, for maximum performance converting large output datasets to Pandas Dataframes, using DuckDB directly may be desirable. However, the difference is typically quite small.  

Four additional libraries improve the DuckDB experience in Jupyter notebooks.  

Pandas  
Clean table visualizations and compatibility with other analysis  
ipython-sql  
Convert a Jupyter code cell into a SQL cell  
SQLAlchemy  
Used by ipython-sql to connect to databases  
duckdb_engine (DuckDB SQLAlchemy driver)  
Used by SQLAlchemy to connect to DuckDB  
```
# Run these pip install commands from the command line if Jupyter Notebook is not yet installed.
# Otherwise, see Google Collab link above for an in-notebook example
pip install duckdb

# Install Jupyter Notebook
pip install notebook

# Install supporting libraries
pip install pandas       # conda install pandas
pip install ipython-sql 
pip install SQLAlchemy
pip install duckdb-engine
```
## Python Create a Database

Startup & Shutdown  
To use the module, you must first create a Connection object that represents the database. The connection object takes as parameter the database file to read and write from. If the database file does not exist, it will be created (the file extension may be .db, .duckdb, or anything else). The special value :memory: (the default) can be used to create an in-memory database. Note that for an in-memory database no data is persisted to disk (i.e. all data is lost when you exit the Python process). If you would like to connect to an existing database in read-only mode, you can set the read_only flag to True. Read-only mode is required if multiple Python processes want to access the same database file at the same time.  
```
import duckdb
# to start an in-memory database
con = duckdb.connect(database=':memory:')
# to use a database file (not shared between processes)
con = duckdb.connect(database='my-db.duckdb', read_only=False)
# to use a database file (shared between processes)
con = duckdb.connect(database='my-db.duckdb', read_only=True)
```
