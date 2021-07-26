"""
# SQLite connection string/uri is a path to the database file - relative or
absolute.
sqlite:///database.db

# MySQL
mysql+pymysql://user:password@ip:port/db_name

# Postgres
postgresql+psycopg2://user:password@ip:port/db_name

# MSSQL
mssql+pyodbc://user:password@dsn_name

# Oracle
oracle+cx_oracle://user:password@ip:port/db_name
"""

import os

class BaseConfig(object):
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'abcdef123456'
  DEBUG = True
  TESTING = False
  FLASK_APP = os.environ.get('FLASK_APP')
  FLASK_ENV = os.environ.get('FLASK_ENV')


class DevConfig(BaseConfig):
  DEBUG = True
  TESTING = True
  SQLALCHEMY_DATABASE_URI = "//test.db" 

class ProdConfig(BaseConfig):
  DEBUG = False
  TESTING = False

class TestConfig(BaseConfig): 
  DEBUG = False
  TESTING = True

  # Database  
  DB_HOST     = os.environ.get('DB_HOST') 
  DB_NAME     = os.environ.get('DB_NAME') 
  DB_PORT     = os.environ.get('DB_PORT')
  DB_USER     = os.environ.get('DB_USER')
  DB_PASSWORD = os.environ.get('DB_PASSWORD')

  #credenciales de prueba 
  DB_HOST       = DB_HOST or 'localhost'  
  DB_NAME       = DB_NAME or 'datospos'   
  DB_USER       = DB_USER or 'usuario2'   
  DB_PASSWORD   = DB_PASSWORD or '123456789'  
  DB_PORT       = DB_PORT or '3306' 

  SQLALCHEMY_DATABASE_URI = "mysql+pymysql://" + DB_USER + ":" + DB_PASSWORD + "@" + DB_HOST + ":" + DB_PORT + "/" + DB_NAME
  SQLALCHEMY_ECHO = False
  SQLALCHEMY_TRACK_MODIFICATIONS = False
