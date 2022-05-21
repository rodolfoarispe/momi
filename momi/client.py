from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from logging import exception
import mysql.connector
import os 


class DataBaseClient():
 
    # Get environment variables
    DB_HOST     = os.getenv('DB_HOST')
    DB_NAME     = os.getenv('DB_NAME')
    DB_USER     = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD') 
    DB_PORT     = os.getenv('DB_PORT')
    DB_DRIVER   = os.getenv('DB_DRIVER')

    connection = None

    def __init__(self, connect=False, usr=DB_USER, pwd=DB_PASSWORD, host=DB_HOST, db=DB_NAME, drv=DB_DRIVER, prt=DB_PORT) -> None:
        #credenciales de prueba 
        self.DB_HOST       = 'localhost'     if host == None else host 
        self.DB_NAME       = 'datospos'      if db   == None else db
        self.DB_USER       = 'usuario2'      if usr  == None else usr 
        self.DB_PASSWORD   = '123456789'     if pwd  == None else pwd 
        self.DB_DRIVER     = 'mysql+pymysql' if drv  == None else drv 
        self.DB_PORT       = '3306'          if prt == None else prt

        if connect==True:
            self.Connect()



    def getEngine(self):
        connStr = '{}://{}:{}@{}:{}/{}'.format( self.DB_DRIVER, 
                                                self.DB_USER, 
                                                self.DB_PASSWORD,
                                                self.DB_HOST, 
                                                self.DB_PORT,
                                                self.DB_NAME)
        engine = create_engine(connStr)
        return engine

    def getSession(self, engine):
        Session = sessionmaker(bind=engine)
        return Session()

    def getCursor(self):
        resp = None
        try:
            resp =  self.connection.cursor()
        except exception as e:
            pass
        return resp 

    def Connect(self):
        config = {
            'user': self.DB_USER,
            'password': self.DB_PASSWORD,
            'host': self.DB_HOST,
            'database': self.DB_NAME,
            'raise_on_warnings': True,
            'buffered':True
            }

        try:
            self.connection =  mysql.connector.connect(**config)
            self.cursor = self.getCursor()
            self.cursor.execute("USE {}".format(self.DB_NAME))

        except mysql.connector.Error as err:
            print(err)
            raise ValueError("Database {} does not exists.".format(self.DB_NAME))
