import mysql.connector
from mysql.connector import errorcode
import os
from datetime import datetime

# Get environment variables
host = os.getenv('DB_HOST')
db = os.getenv('DB_NAME')
usr = os.getenv('DB_USER')
pwd = os.getenv('DB_PASSWORD') 

DB_HOST     = 'localhost' if host == None else host 
DB_NAME     = 'datospos'   if db == None else db
DB_USER     = 'usuario2'  if usr == None else usr 
DB_PASSWORD = '123456789' if pwd == None else pwd 

config = {
    'user': DB_USER,
    'password': DB_PASSWORD,
    'host': DB_HOST,
    'database': DB_NAME,
    'raise_on_warnings': True
    }

def registrarVentaContado(cia, pedido, respuesta):
    
    estatus = 'OK' if respuesta['isSuccess'] == 'true' else 'KO'
    mensaje = ''
    for x in respuesta.get('mensajes'):
        #mensaje =  mensaje + ' | ' if mensaje!='' else '' + ('%s = %s: %s / %s: %s ' % ( pedido, estatus,  x['tipo'] , x['codigo'] , x['mensaje'] ) )
        mensaje =  mensaje + ' | ' if mensaje!='' else '' + ('%s / %s: %s ' % (  x['tipo'] , x['codigo'] , x['mensaje'] ) )
    internalId = respuesta.get('internalId')
    internalId = 'Null' if internalId == None else internalId

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()


    try:
        cursor.execute("USE {}".format(DB_NAME))

    except mysql.connector.Error as err:
        print("\nDatabase {} does not exists.".format(DB_NAME))
        print(err)
        exit(1)

    try:
        sql = """
                   insert into registro (rcp_cia, rcp_pedido, reg_grupo, reg_resultado, reg_estatus, reg_internalId) 
                                values ('{cia}','{num}', '{grp}', '{res}','{sta}', {iid}) 
                    on duplicate key update
                            reg_resultado = '{res}', reg_estatus = '{sta}', reg_fecha_modificacion = now()

               """.format(cia=cia, num=pedido, grp='CASH_SALE', res=mensaje, sta=estatus, iid=internalId )

        cursor.execute(sql) 
        cnx.commit()

        print ("\n",datetime.now().strftime("%Y-%m-%d %H:%M:%S"), pedido, mensaje, end='')
                                
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("\nSomething is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("\nDatabase does not exist")
        else:
            print(err)
    else:
        cnx.close()
    
