from sqlalchemy import Column, String, Integer, Boolean, declarative_base

Base = declarative_base()

class regMonitor(Base):
    nombre = Column(String(100), primary_key=True)
    descripcion = Column(String, nullable=True)
    encendido = Column(Boolean, default=False )
    
