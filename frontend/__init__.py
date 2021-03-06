

# Libraries
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from datetime import datetime 

# Config
from .config import DevConfig, TestConfig

import procesar_items as   proc_items
import procesar_ordenes as proc_orders
import validar_ordenes as  check_orders
import venta_contado_buc as proc_cash

# Globals

db = SQLAlchemy()

socketio = SocketIO(async_mode='threading')



# Factory
def init_app():
    app = Flask(__name__)

    #----INI: Se definen filtros
    @app.template_filter()
    def strftime(date, fmt=None):
        format='%Y-%m-%d'
        return date.strftime(format) 
    #----FIN: Se definen filtros

    app.config.from_object(TestConfig)
    
    db.init_app(app)
    
    with app.app_context():

        #importamos los blueprints
        from .main import main
        from .admin import admin
        from .auth import auth
        
        #registramos los blueprints
        app.register_blueprint(main.main_bp)
        app.register_blueprint(admin.admin_bp)
        app.register_blueprint(auth.auth_bp)

        #db.Model.metadata.reflect(bind=db.engine, schema=app.config.get('DB_NAME'))  #reflejar las tablas y vistas 
        #db.metadata.reflect(bind=db.engine,  schema=app.config.get('DB_NAME'), views=True) #reflect tables and views 

        db.create_all()

        socketio.init_app(app)


        return app 
