from datetime import datetime, timedelta

class regAbono:
    def __init__(self, registro=None) -> None:

        self.num_pedido        = None
        self.num_documento     = None
        self.num_abono         = None
        self.fecha             = None 
        self.monto             = None
        self.usuario           = None  
        self.metodo_pago       = None 
        self.ubicacion         = None


        if registro != None:
            self.cargarDatos(registro)

    def cargarDatos(self, registro):
        self.num_pedido            = registro.get('abo_pedido')     #pedido
        self.num_documento         = registro.get('abo_documento')  #interal id de la orden
        self.num_abono            = registro.get('abo_secuencia')   #secuencial del abono

        fecha = registro.get('fecha_registro')
        hora  = registro.get('hora_registro')
        self.fecha     = fecha + hora

        self.monto       = registro.get('abo_monto')
        self.usuario     = registro.get('abo_usuario')
