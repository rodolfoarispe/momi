import mysql.connector
import os 


class DataBaseClient():
 
    # Get environment variables
    DB_HOST     = os.getenv('DB_HOST')
    DB_NAME     = os.getenv('DB_NAME')
    DB_USER     = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD') 

    connection = None

    def __init__(self, connect=False, usr=DB_USER, pwd=DB_PASSWORD, host=DB_HOST, db=DB_NAME) -> None:
        #credenciales de prueba 
        self.DB_HOST       = 'localhost'  if host == None else host 
        self.DB_NAME       = 'datospos'   if db   == None else db
        self.DB_USER       = 'usuario2'   if usr  == None else usr 
        self.DB_PASSWORD   = '123456789'  if pwd  == None else pwd 

        if connect==True:
            self.Connect()


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
            self.cursor = self.connection.cursor()
            self.cursor.execute("USE {}".format(self.DB_NAME))

        except mysql.connector.Error as err:
            print(err)
            raise ValueError("Database {} does not exists.".format(self.DB_NAME))
