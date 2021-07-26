
"""
Prueba de venta contado con cabecera en una ubicación y artículos en otra diferente
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

from venta_contado_put import subirVentaContado
from momi.t_cabecera import regCabecera
from momi.t_detalle import regDetalle

from datetime import datetime, timedelta 

#CABECERA
master = regCabecera()
details = []


master.num_cuenta     = None
master.num_factura    = 'TEST-0022'
master.fecha_transacc = datetime(2021,4,20)
#master.fecha_efectiva = datetime(2020,2,29)
master.estatus        = 4 #??
master.cod_ubicacion  =  21
master.cod_cliente    = 12 #cliente anonimo
master.cod_fiscal     = 'ABCXYZ-0022'
#master.cod_vendedor   = 7202
master.metodo_pago = 5


#ARTICULOS  
item1 = regDetalle()
item1.cantidad     = 1
item1.cod_articulo = 4088
item1.descripcion  = 'bebida de avena'
item1.linea        = 1
item1.location     = 17
item1.precio       = 0.75
details.append(item1) 


item2 = regDetalle()
item2.cantidad     = None
item2.cod_articulo = 2198
item2.descripcion  = 'desc dulc'
item2.linea        = 2
item2.location     = 21
item2.precio       = 0.15
details.append(item2) 


item3 = regDetalle()
item3.cantidad     = 1
item3.cod_articulo = 4432
item3.descripcion  = 'velas regulares'
item3.linea        = 3
item3.location     = 21
item3.precio       = 0.75
details.append(item3)


item4 = regDetalle()
item4.cantidad     = None
item4.cod_articulo = 2199
item4.descripcion  = 'desc jub'
item4.linea        = 4
item4.location     = 21
item4.precio       = 2.00
details.append(item4) 


item5 = regDetalle()
item5.cantidad     = 2
item5.cod_articulo = 4007
item5.descripcion  = 'cake de vainilla de 9"'
item5.linea        = 5
item5.location     = 17
item5.precio       = 19.50
details.append(item5) 


item6 = regDetalle()
item6.cantidad     = 1
item6.cod_articulo = 5951
item6.descripcion  = 'agua aqua viva'
item6.linea        = 6
item6.location     = 21
item6.precio       = 1.00
#details.append(item6) 


item7 = regDetalle()
item7.cantidad     = 2
item7.cod_articulo = 4006
item7.descripcion  = 'cake de vainilla de 7"'
item7.linea        = 6
item7.location     = 17
item7.precio       = 12.95
details.append(item7) 


try:
    resp = subirVentaContado (master, details)
    
    internal =  resp.get('internalId') if resp.get('isSuccess') == 'true' else 'Err'

    for x in resp.get('mensajes'):
        print('%s / internal: %s -> %s: %s ' % (  master.num_factura,  internal  , x.get('codigo') ,  x.get('mensaje')))
except Exception as e:
    print (e.args[0])