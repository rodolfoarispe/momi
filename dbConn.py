from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, MetaData

import os

Base = declarative_base()

# Get environment variables
env_host = os.getenv('DB_HOST')
env_db = os.getenv('DB_NAME')
env_usr = os.getenv('DB_USER')
env_pwd = os.getenv('DB_PASSWORD') 
env_driver = os.getenv('DB_DRIVER')

DB_HOST     = 'localhost'     if env_host    == None else env_host 
DB_NAME     = 'datospos'      if env_db      == None else env_db
DB_USER     = 'usuario2'      if env_usr     == None else env_usr 
DB_PASSWORD = '123456789'     if env_pwd     == None else env_pwd 
DB_DRIVER   = 'mysql+pymysql' if env_driver  == None else env_driver

#engine = create_engine('sqlite:///productos.sqlite')
engine = create_engine('{driver}://{user}:{pwd}@{srv}/{db}'.format(
                    driver=DB_DRIVER, 
                    user=DB_USER,
                    pwd=DB_PASSWORD,
                    srv=DB_HOST,
                    db=DB_NAME))

# refleja todas las clases que estén cargadas en el momento
# DeferredReflection.prepare(engine)

metadata = MetaData(bind=engine)

#REFLEJAMOS LAS TABLAS QUE FUERON CREADAS MANUALMENTE
#metadata.reflect(engine, only=['rcpedidos', 'rdpedidos'])


#Base.metadata = metadata
Session = sessionmaker(bind=engine)

