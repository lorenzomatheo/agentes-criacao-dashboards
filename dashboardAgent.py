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
import logging


def extract_csv_data(filepath):
    """Extrai dados de um arquivo CSV."""
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        logging.error(f"Erro ao extrair CSV: {e}")
        return None

def create_db_engine(filepath):
    """Cria um engine SQLAlchemy para se conectar ao banco de dados."""
    try:
        engine = create_engine(filepath)
        logging.info(f"Engine criada com sucesso para: {filepath}")
        return engine
    except SQLAlchemyError as e:
        logging.error(f"Erro ao criar engine para {filepath}: {e}")
        return None
    
def create_session(engine):
    """Criação de um sessiomaker associado a engine, retornando uma session"""
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        logging.info("Sessão criada com sucesso.")
        return session
    except SQLAlchemyError as e:
        logging.error(f"Erro ao criar sessão: {e}")
        return None


def extract_sql_data(session, query):
    """Extrai dados de um banco de dados SQL usando SQLAlchemy e session."""
    try: 
        result = session.execute(text(query))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        logging.info(f"Dados extraídos com sucesso do banco de dados. Query: {query}")
        return df
    except SQLAlchemyError as e:
        logging.error(f"Erro ao extrair dados do banco de dados: {e}")
        return None
    except Exception as e:
        logging.error(f"Erro inesperado ao extrair dados: {e}")
        return None


