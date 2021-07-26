class regDetalle: 
    def __init__(self, registro=None) -> None:
        self.cod_articulo       = None        
        self.cantidad           = None 
        self.descripcion        = None    
        self.precio             = None
        self.linea              = None
        self.location           = None 

        if registro != None:
            self.cargarDatos(registro)

    def cargarDatos(self, registro):
        self.cod_articulo   = registro.get('rdp_producto')  
        self.cantidad       = registro.get('rdp_cantidad')        
        self.descripcion    = registro.get('rdp_comentario')   
        self.precio         = registro.get('rdp_precio')
        self.linea          = registro.get('rdp_linea')
          
