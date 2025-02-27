import pandas as pd
import os
import plotly.express as px
import dash
from dash import dcc, html
import requests
import os
import json
from datetime import datetime

from langchain.llms import openai
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor
import openai

import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import logging



openai_api_key = os.getenv('OPENAI_API_KEY')


llm = ChatOpenAI(model="gpt-3.5-turbo")



def extract_csv_data(filepath):
    """Extrai dados de um arquivo CSV."""
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        logging.error(f"Erro ao extrair CSV: {e}")
        return None

def create_db_engine(df: pd.DataFrame) -> 'sqlalchemy.engine.Engine' | None:
    """Cria um engine SQLAlchemy para se conectar ao banco de dados."""
    if df is None:
        logging.error("DataFrame inválido para criar o banco.")
        return None
    
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


def create_sql_agent_from_session(session,engine):
    """ Criação de Agente SQL com LangChain a partir da session do SQLALchemy"""
    if session is None:
        logging.error("Sessão SQLAlchemy inválida para criar o agente SQL")
        return None
    
    try:
        # Cria uma instância do SQLDataBase a partir da engine
        
        db = SQLDatabase(engine=engine)
        
        # Cria a toolkit
        
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)

        # Cria o agente executor
        agent_executor = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=True
        )

        logging.info("Agente SQL criado com sucesso!")
        
        return agent_executor
    
    except Exception as e:
        logging.error(f"Erro ao criar Agente SQL: {e}")
        return None

# Pendente 1 
def query_with_langchain(agent_executor, user_query):
    """Interagem com um banco de dados usando um agente LangChain e uma consulta em linguagem natural"""
    if agent_executor is None:
        logging.error("AgentExecutor inválido fornecido.")
        return None
    
    if not user_query or not isinstance(user_query, str):
        logging.error("Consulta do usuário inválida ou vazia.")
        return None

    try:
        logging.info(f"Executando consulta: {user_query}")
        result = agent_executor.run(user_query)  # Executa a consulta com o agente
        logging.info("Consulta executada com sucesso.")
        return result
    
    except Exception as e:
        logging.error(f"Erro ao executar a consulta '{user_query}': {e}")
        return None


# Pendente 2
# Integração LangChain com fluxo de trabalho

# Pendente 3
# Interface com Streamlit()




