import time 
import json
from flask_socketio import SocketIO, emit
from .. import socketio

from .. import proc_items
from .. import proc_orders
from .. import check_orders
from .. import proc_cash

@socketio.on('proceso')
def handle_my_custom_event(input_json):
    opcion =  input_json.get('data')

    if opcion == 'items':
        txt = 'Iniciando el proceso: ' + opcion + '<br>La descarga puede tomar varios minutos.<br>Por favor espere...'
        emit ('items.procesando', json.dumps({'data': {'cantidad':0}}))
        emit ('items.mensajes', json.dumps({'data': txt}) ) 

        x = proc_items.main(socketio)

        socketio.start_background_task(target=x)  
        
        #time.sleep(5)
        emit ('items.procesado', json.dumps({'data':'Proceso Terminado!<br>La p&aacute;gina se refresacar&aacute; en segundos' }) )

    if opcion == 'orders':
        txt = 'Iniciando el proceso: ' + opcion + '<br>La descarga puede tomar varios minutos.<br>Por favor espere...'
        emit ('orders.procesando', json.dumps({'data': {'cantidad':0, 'lineas':0}}))
        emit ('orders.mensajes', json.dumps({'data': txt}) ) 

        x = proc_orders.main(socketio)
        y = check_orders.main(socketio)

        socketio.start_background_task(target=x)  
        socketio.start_background_task(target=y)  
        
        #time.sleep(5)
        emit ('orders.procesado', json.dumps({'data':'Proceso Terminado!<br>La p&aacute;gina se refresacar&aacute; en segundos' }) )


    if opcion == 'cash':
        chk =  input_json.get('chk')
        txt = 'Iniciando el proceso: ' + opcion  + '<br>La carga puede tomar varios minutos.<br>Por favor espere...'
        emit ('cashsale.procesando', json.dumps({'data': {'cantidad':0, 'lineas':0}}))
        emit ('cashsale.mensajes', json.dumps({'data': txt}) ) 

        x = proc_cash.Procesar('NW', socketio)
        y = proc_cash.Procesar('KO', socketio)

        socketio.start_background_task(target=x)  
        if chk: 
            socketio.start_background_task(target=y)  

        emit ('cashsale.procesado', json.dumps({'data':'Proceso Terminado!<br>La p&aacute;gina se refresacar&aacute; en segundos' }) )
