
from logging import raiseExceptions
import mysql.connector
from mysql.connector import errorcode
import os

from mysql.connector.cursor import MySQLCursor

from momi import regCabecera, regDetalle


def buscarVentasCredito(cnx, grupo='NW'):
    cursor = cnx.cursor()

    try:
       cursor.execute("""
                        select * from vi_venta_credito_pend where ifnull(reg_estatus,'NW') = '{}'
                      """.format(grupo) )

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


    return cursor 



def leerVentaCredito(cnx, cursor:MySQLCursor):
    master = None 
    details = []
    resp = {'cabecera':None, 'detalle':[] } 

    try:
        row1 = cursor.fetchone()

        if row1 != None:

            cabecera = dict(zip(cursor.column_names, row1)) 

            cia = cabecera['rcp_cia']
            cod = cabecera['rcp_pedido']
    
            cursor2 = cnx.cursor()
            sql =  """
                        select * from vi_rdpedidos 
                        where binary rdp_cia = '{x}' 
                        and binary rdp_pedido = '{y}'
                        order by rdp_linea
                    """.format(x=cia, y=cod)

            cursor2.execute (sql)
            result2 = cursor2.fetchall()
            
            for row2 in result2:
                detalle = dict(zip(cursor2.column_names, row2)) 

                master = regCabecera(cabecera)
                details.append(regDetalle(detalle))
                
            cursor2.close()
            
            resp['cabecera'] = master 
            resp['detalle'] = details

    except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
   # else:
   #     cnx.close()

    return resp 

if __name__ == "__main__":
    pass
  # registro = leerVentaContado()
  # print (registro['cabecera'])
  # print (registro['detalle'])