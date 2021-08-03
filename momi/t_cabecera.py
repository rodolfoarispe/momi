from datetime import datetime, timedelta
import dbConn as db

# se definen clases que seran reflejadas
class tblRcpedidos (db.DeferredReflection, db.Base):
    __tablename__ = 'rcpedidos'

class regCabecera:
    def __init__(self, registro=None) -> None:

        self.num_cia            = None  
        self.num_factura        = None  
        self.num_cuenta         = None      
        self.fecha_transacc     = None
        self.fecha_efectiva     = None        
        self.estatus            = None    
        self.cod_ubicacion      = None    
        self.cod_cliente        = None    
        self.cod_fiscal         = None    
        self.cod_vendedor       = None
        self.comentario         = None
        self.tipo_registro      = None
        self.metodo_pago1       = None
        self.metodo_pago2       = None
        self.monto_pago1        = None 
        self.monto_pago2        = None
        self.nombre_pago2       = None
        self.identif_pago2      = None


        if registro != None:
            self.cargarDatos(registro)

    def cargarDatos(self, registro):
        self.num_cia            = registro.get('rcp_cia')  
        self.num_factura        = registro.get('rcp_pedido')   
        #self.num_cuenta         = registro.get('num_cuenta')   
        
        #fecha = datetime.strptime(registro.get('fecha_registro'),'%m/%d/%Y') #TODO la bd deberia ser fecha.  se hizo string por problemas de importacion
        fecha = registro.get('fecha_registro')
        hora  = registro.get('hora_registro')
        self.fecha_transacc     = fecha + hora

        self.fecha_efectiva     = self.fecha_transacc     
           
        self.estatus            = registro.get('rcp_status')
        self.cod_ubicacion      = registro.get('rcp_entregar')
        self.cod_cliente        = registro.get('rcp_cliente') 
        self.cod_fiscal         = registro.get('rcp_anulado_por') 
        self.cod_vendedor       = registro.get('rcp_vendedor')
        self.comentario         = registro.get('rcp_comentario')
        self.tipo_registro      = registro.get('rcp_salida') #FA = FACTURA, NC=REVERSO, OV=ORDEN DE VENTA
        self.metodo_pago1       = registro.get('rcp_imput1')
        self.metodo_pago2       = registro.get('rcp_imput2')
        self.monto_pago1        = registro.get('rcp_impuesto1')
        self.monto_pago2        = registro.get('rcp_impuesto2')
        