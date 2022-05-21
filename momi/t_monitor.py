from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import  declarative_base

Base = declarative_base()

class regMonitor(Base):
    __tablename__ = 'monitor'
    nombre = Column(String(100), primary_key=True)
    descripcion = Column(String(500), nullable=True)
    disponible = Column(String(100), nullable=False, default='S' )
    usuario = Column(String(100), nullable = True)

    def __init__(self, nombre, **kwargs) -> None:
        super().__init__()
        self.nombre = nombre
        for key, value in kwargs.items():
            setattr(self, key, value)


    def __actualizarFlag(self, engine, session, flag ):
        regMonitor.__table__.create(bind=engine, checkfirst=True) #se crea la tabla si no existe
        registro = session.query(regMonitor).filter(regMonitor.nombre==self.nombre).one_or_none()
        if registro != None :
            if registro.disponible not in ['N','S']: 
                print ('El proceso no puede ejecutars en este momento.  Flag no es N ni S')
                return False
            else:
                registro.disponible = flag
                self = registro 
        else:
            self.disponible = flag
            session.add(self)            
    
        session.commit()

        return True 

    def activarFlag(self, engine, session):
        return self.__actualizarFlag(engine, session, 'S')


    def desactivarFlag(self, engine, session):
        return self.__actualizarFlag(engine, session, 'N')
