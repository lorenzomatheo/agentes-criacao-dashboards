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
if not openai_api_key:
    raise ValueError("Chave da API OpenAI não encontrada.")


llm = ChatOpenAI(model="gpt-3.5-turbo")



def extract_csv_data(contents: str, filepath: str) -> pd.DataFrame | None:
    """Extrai dados de um arquivo CSV."""
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        logging.error(f"Erro ao extrair CSV: {e}")
        return None

def extract_excel_data(filepath: str) -> pd.DataFrame | None:
    """Extrai dados de um arquivo Excel."""
    try:
        df = pd.read_excel(filepath)
        return df
    except Exception as e:
        logging.error(f"Erro ao extrair Excel: {e}")
        return None
    
def transform_data(df: pd.DataFrame) -> pd.DataFrame | None:
    """Transforma e limpa dados"""
    if df is None or not isinstance(df, pd.DataFrame):
        logging.error("DataFrame inválido para tratar os dados.")
        return None
    try:
        transformed_df = df.copy()
        initial_rows = len(transformed_df)
        logging.info(f"Iniciando transformação com {initial_rows} linhas e {len(transformed_df.columns)} colunas.")
        
        # Remover linhas com valores nulos em colunas críticas (ajuste os nomes)
        if critical_columns is None:
            critical_columns = [col for col in transformed_df.columns if 'id' in col.lower() or 'valor' in col.lower()]
        if critical_columns:
            transformed_df.dropna(subset=critical_columns, inplace=True)
            logging.info(f"Removidas {initial_rows - len(transformed_df)} linhas com nulos em {critical_columns}.")

        # Padronizar nomes de colunas (remover espaços, letras minúsculas)
        transformed_df.columns = [col.strip().replace(' ', '_').lower() for col in transformed_df.columns]
        logging.info("Nomes de colunas padronizados.")

        # Converter tipos de dados caso necessário(Tipo de data por exemplo)
        for col in transformed_df.columns:
            if "data" in col or "date" in col:
                transformed_df[col] = pd.to_datetime(transformed_df[col], errors='coerce')
            elif transformed_df[col].dtype == 'object':
                try:
                    transformed_df[col] = pd.to_numeric(transformed_df[col], errors='coerce')
                except ValueError:
                    pass  # Ignora se não for conversível


        # Remover duplicatas, se aplicável
        initial_rows = len(transformed_df)
        transformed_df.drop_duplicates(inplace=True)
        logging.info(f"Removidas {initial_rows - len(transformed_df)} duplicatas.")

        logging.info(f"Transformação concluída: {len(transformed_df)} linhas restantes.")
        return transformed_df
    
    except Exception as e:
        logging.error(f"Erro ao transformar os dados: {e}")
        return None


def create_db_engine(df: pd.DataFrame) -> 'sqlalchemy.engine.Engine' | None:
    """Cria um engine SQLAlchemy para se conectar ao banco de dados."""
    if df is None:
        logging.error("DataFrame inválido para criar o banco.")
        return None
    try:
        # Criar um banco SQLite em memória
        engine = create_engine("sqlite:///:memory:")
        # Salvar o DataFrame como uma tabela chamada 'data_table'
        df.to_sql("data_table", engine, if_exists="replace", index=False)
        logging.info("Engine criada e banco preenchido com sucesso.")
        return engine
    except SQLAlchemyError as e:
        logging.error(f"Erro ao criar engine ou preencher o banco: {e}")
        return None
    
def create_session(engine) -> 'sqlalchemy.orm.Session' | None:
    """Criação de um sessiomaker associado a engine, retornando uma session"""
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        logging.info("Sessão criada com sucesso.")
        return session
    except SQLAlchemyError as e:
        logging.error(f"Erro ao criar sessão: {e}")
        return None


def create_sql_agent_from_session(session,engine) -> 'AgentExecutor' | None:
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


def query_with_langchain(agent_executor, user_query: str) -> str | None:
    """Interagem com um banco de dados usando um agente LangChain e uma consulta em linguagem natural"""
    if agent_executor is None or not user_query or not isinstance(user_query, str):
        logging.error("Agente ou consulta inválida.")
        return None
    try:
        logging.info(f"Executando consulta: {user_query}")
        result = agent_executor.run(user_query)  # Executa a consulta com o agente
        logging.info("Consulta executada com sucesso.")
        return result
    
    except Exception as e:
        logging.error(f"Erro ao executar a consulta '{user_query}': {e}")
        return None





