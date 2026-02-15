import datetime as dt
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.empty import EmptyOperator
from elasticsearch import Elasticsearch
from elasticsearch import helpers

import psycopg2 as db

import pandas as pd

# function untuk ambil data dari postgresql
def fetch_postgre():
    """
    Fetches all data from the `table_m3` table in a PostgreSQL database
    using predefined credentials, then saves the result to a CSV file.

    Process:
    - Establishes a connection to the PostgreSQL database with the following configuration:
        database : "airflow"
        user     : "airflow"
        password : "airflow"
        host     : "postgres"
        port     : "5432"
    - Executes the query: SELECT * FROM table_m3
    - Saves the query result as a CSV file at:
        /opt/airflow/dags/P2M3_rexy_nurulsaputra_data_raw.csv
    """

    conn = db.connect(
        database="postgres",
        user='airflow',
        password='airflow',
        host='postgres',
        port='5432')
    
    data = pd.read_sql('Select * from table_m3', con = conn)
    
    # save as csv
    data.to_csv('/opt/airflow/dags/P2M3_muhammad_damar_data_raw.csv', index=False)

# function untuk read dan cleaning csv
def clean_data():
    """
    Cleans the raw dataset exported from PostgreSQL and saves the cleaned version to a CSV file.

    Process
    - Reads the raw CSV file located at:
        /opt/airflow/dags/P2M3_rexy_nurulsaputra_data_raw.csv
    - Removes rows with missing values.
    - Removes duplicate rows.
    - Cleans column names by:
        * Remove        '(' and ')'
        * Replacing     '%' with 'percent'
        * Stripping     whitespace
        * Replacing     '-' with space 
        * Replacing     spaces with '_'
        * Converting to lowercase
    - Converts the 'launch_date' column to datetime format.
    - Saves the cleaned DataFrame to:
        /opt/airflow/dags/P2M3_rexy_nurulsaputra_data_clean.csv
    """

    df = pd.read_csv('/opt/airflow/dags/P2M3_muhammad_damar_data_raw.csv')
    df = df.dropna()
    df = df.drop_duplicates()
    df.columns = (df.columns
                .str.replace('(', '')  
                .str.replace(')', '')  
                .str.replace('%', 'percent') 
                .str.strip()
                .str.replace('-', ' ')
                .str.replace(' ', '_')
                .str.lower())  
        
    df.to_csv('/opt/airflow/dags/P2M3_muhammad_damar_data_clean.csv', index=False)

# upload data to elasticsearch
def load_elastic():
    """
    Uploads the cleaned dataset into an Elasticsearch index.

    Process
    - Connects to the Elasticsearch at http://elasticsearch:9200
    - Reads the cleaned CSV file located at /opt/airflow/dags/P2M3_rexy_nurulsaputra_data_clean.csv
    - Converts each row of the DataFrame into a dictionary.
    - Prepares bulk upload actions with:
        * Index name: "this_table_m3"
        * Document source: row data
    - Executes a bulk insert into Elasticsearch using the helpers.bulk API.
    """
    
    # connect ke elastic
    es = Elasticsearch("http://elasticsearch:9200")
    df = pd.read_csv('/opt/airflow/dags/P2M3_muhammad_damar_data_clean.csv')

    # ubah semua baris jadi list of dict
    records = df.to_dict(orient="records")

    # actions untuk bulk upload
    actions = []
    for doc in records:
        action = {
            "_index": "table_m3v2",   
            "_source": doc       
        }
        actions.append(action)

    # bulk insert ke elastic
    response = helpers.bulk(es, actions)
    print(response)

default_args = {
    'owner': 'damar',
    'start_date': dt.datetime(2024, 11, 1),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1),
}


with DAG('FINALM7',
         default_args=default_args,
         schedule_interval='10,20,30 9 * 11 6',      # '0 * * * *',
         ) as dag:
    
    fetchPostgre = PythonOperator(task_id='fetch_postgre_data',
                                 python_callable=fetch_postgre)
    
    cleanData = PythonOperator(task_id='clean_data',
                                 python_callable=clean_data)
    
    uploadElastic = PythonOperator(task_id='upload_to_elastic',
                                 python_callable=load_elastic)

fetchPostgre >> cleanData >> uploadElastic 