import pandas as pd
import os
import plotly.express as px
import dash
from dash import dcc, html
import requests
import os
import json
from datetime import datetime

from langchain import * 
import openai

import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import psycopg2

def extract_csv_data(filepath):
    """Extrai dados de um arquivo CSV."""
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        print(f"Erro ao extrair CSV: {e}")
        return None

def extract_sql_data(database_path, query):
    """Extrai dados de um banco de dados ."""
    try: 
        db = session.query(filepath)
        return db
    except Exception as e:
        print(f"Erro ao extrair CSV: {e}")
        return None


