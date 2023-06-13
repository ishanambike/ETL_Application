import pandas as pd
import numpy as np
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from sqlalchemy import URL
from flask import Flask

app = Flask('etl')

# Function to write contents of final table in DB
def writeToDb(usersDF):

    # Getting credentials and database name from .env file
    username = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    dbName = os.getenv('POSTGRES_DB')



    conn = psycopg2.connect(host = "host.docker.internal", port = "5432", user = username, password = password)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    checkIfDbExists = "SELECT datname FROM pg_catalog.pg_database WHERE datname = '" + dbName + "';" # checking if DB exists
    dbDF = pd.read_sql(checkIfDbExists, con = conn)


    if dbDF.size == 0: # if DB doesn't exists then creating the DB
        sqlCreateDatabase = "create database " + dbName + ";"
        cursor.execute(sqlCreateDatabase)

    conn.commit()
    cursor.close()
    conn.close()

    url_object = URL.create(
        "postgresql+psycopg2",
        username=username,
        password=password,
        host="host.docker.internal",
        port='5432',
        database=dbName,
    )

    engine = create_engine(url_object)

    usersDF.to_sql( # writing data in users table
        'users',
        con = engine,
        if_exists='replace',
        index=False
    )





def etl():
    # Load CSV files
    # Process files to derive features
    # Upload processed data into a database

    # importing data
    usersDF = pd.read_csv('data/users.csv')
    experimentsDF = pd.read_csv('data/user_experiments.csv')
    compoundsDF = pd.read_csv("data/compounds.csv")

    # removing whitespace from column names
    usersDF.columns = usersDF.columns.str.strip()
    experimentsDF.columns = experimentsDF.columns.str.strip()
    compoundsDF.columns = compoundsDF.columns.str.strip()

    # removing whitespace from column values
    stringColsList = list(usersDF.select_dtypes(['object']).columns)
    for colName in stringColsList:
        usersDF[colName] = usersDF[colName].str.strip()

    stringColsList = list(experimentsDF.select_dtypes(['object']).columns)
    for colName in stringColsList:
        experimentsDF[colName] = experimentsDF[colName].str.strip()

    stringColsList = list(compoundsDF.select_dtypes(['object']).columns)
    for colName in stringColsList:
        compoundsDF[colName] = compoundsDF[colName].str.strip()



    # 1.Total experiments a user ran.
    totalEexperiments = experimentsDF.groupby('user_id').size()
    totalEexperimentsDF = pd.DataFrame({'user_id' : totalEexperiments.index, 'total_experiments' : totalEexperiments.values})
    usersDF = usersDF.merge(totalEexperimentsDF, on = 'user_id', how = 'left')

    # 2.Average experiments amount per user.
    usersDF['average_experiments'] = experimentsDF.groupby('user_id').size().mean()



    # 3.User's most commonly experimented compound.
    commonCompoundDF = experimentsDF.groupby('user_id')['experiment_compound_ids'].apply(lambda x: x.str.split(';').explode().mode()).reset_index()
    commonCompoundDF.drop(columns = ['level_1'], inplace = True)
    commonCompoundDF.rename(columns = {'experiment_compound_ids': 'compound_id'}, inplace = True)
    commonCompoundDF.drop_duplicates(subset = 'user_id', keep = False, inplace = True) # removing user_id columns with multiple records as there is no mode

    commonCompoundDF["compound_id"] = commonCompoundDF["compound_id"].astype('int64')
    usersDF = usersDF.merge(commonCompoundDF, on = 'user_id', how = 'left')

    usersDF = usersDF.merge(compoundsDF, on = 'compound_id', how = 'left') # joining with compoundsDF to get compound names

    usersDF.drop(columns=['compound_id', 'compound_structure'], inplace = True)
    usersDF.rename(columns={'compound_name': 'most_common_compound'}, inplace = True)
    usersDF['most_common_compound'] = usersDF['most_common_compound'].replace(np.nan, "NA") # setting NA when there is no most commonly experimented compound

    # calling function to write data into the DB
    writeToDb(usersDF)







# Your API that can be called to trigger your ETL process
@app.route('/')
def trigger_etl():
    # Trigger your ETL process here
    etl()
    return {"message": "ETL process started"}, 200
