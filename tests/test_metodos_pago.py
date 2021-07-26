
"""
Prueba de los métodos de pago

1	EFECTIVO
2	CHEQUE
18	MASTER CARD
19	VISA
20	AMERICAN EXPRESS
7	ACH
8	CLAVE
11	DEPOSITO
12	YAPPY
13	E-C. VISA
14	E-C. ACH
15	E-C. YAPPY
16	E-C. MASTER CARD
17	E-C. AMERICAN EXPRESS


"""

#-- agregando el directorio padre
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
#----


import venta_contado_put as venta
import momi.t_cabecera as cab
import momi.t_detalle as det 


from datetime import datetime, timedelta 

#CABECERA
master = cab.regCabecera()
details = []

secuencial = datetime.now().strftime("%y%m%d%H%M%S")

master.num_cuenta     = None
master.num_factura    = 'TEST-' + secuencial
master.fecha_transacc = datetime(2021,4,20)
master.estatus        = 4 #??
master.cod_ubicacion  =  21
master.cod_cliente    = 12 #cliente anonimo
master.cod_fiscal     = 'ABCXYZ-' + secuencial
master.cod_vendedor   = 7202
master.metodo_pago1 = 2
master.metodo_pago2 = 19
master.monto_pago1 = 29.50
master.monto_pago2 = 9.50

#ARTICULOS  

item1 = det.regDetalle()
item1.cantidad     = 2
item1.cod_articulo = 4007
item1.descripcion  = 'cake de vainilla de 9"'
item1.linea        = 1
item1.location     = 17
item1.precio       = 19.50
details.append(item1) 


try:
    resp = venta.subirVentaContado (master, details)
    
    internal =  resp.get('internalId') if resp.get('isSuccess') == 'true' else 'Err'

    for x in resp.get('mensajes'):
        print('%s / internal: %s -> %s: %s ' % (  master.num_factura,  internal  , x.get('codigo') ,  x.get('mensaje')))
except Exception as e:
    print (e.args[0])