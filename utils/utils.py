import snowflake.connector
import pandas as pd
import streamlit as st
import yaml

def read_yaml(file_path="./config.yaml"):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(**st.secrets["snowflake"])

@st.experimental_memo(ttl=7200)
def execute_statement(sql, _conn):
    with _conn.cursor() as cur:
        cur.execute(sql)

@st.experimental_memo(ttl=3600)
def run_query(sql, _conn):
    with _conn.cursor() as cur:
        cur.execute(sql)
        all_rows = cur.fetchall()
#        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]
        df = pd.DataFrame(all_rows)
        try:
            df.columns = field_names
        except ValueError:
            pass
        return df        

from IPython.display import Markdown, display
def printmd(string):
    display(Markdown(string))


def create_link(kbc_component_configuration_id, jobs_df):
    """
    

    Parameters
    ----------
    kbc_component_configuration_id : id of a config
        DESCRIPTION.
    jobs_df : pandas dataframe
        it contains data from jobs table joined with configurations table

    Returns
    -------
    hyperlink : string
        hyperlink for a config id

    """    
    _,_,_, configuration = kbc_component_configuration_id.split('_')        
    link = jobs_df.loc[jobs_df.kbc_component_configuration_id==kbc_component_configuration_id, "kbc_component_configuration_url"].values[0]                    
    hyperlink = f'<a target="_blank" href="{link}">{configuration}</a>'  
    return hyperlink 


def calculate_monthly_change(df, column):
    """
    Calculate last month value and difference against the month before
    

    Parameters
    ----------
    df : dateframe with datetime index
    column : numeric column

    Returns
    -------
    tuple of (value for last month, change of last month value with respect to the month before)

    """
    try:
        last_month = df.index[-2]
        last_value = int(df.at[last_month, column])
    except IndexError:
        last_value = 'NA'
    
    try:
        penultimate_month = df.index[-3]
        difference = int(df.at[last_month, column] - df.at[penultimate_month, column]) 
    except IndexError:
        difference = 'NA'
    return last_value, difference 