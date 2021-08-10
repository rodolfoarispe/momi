import mysql.connector
from mysql.connector import errorcode
import os

# Get environment variables
host = os.getenv('DB_HOST')
db = os.getenv('DB_NAME')
usr = os.getenv('DB_USER')
pwd = os.getenv('DB_PASSWORD') 

DB_HOST     = 'localhost' if host == None else host 
DB_NAME     = 'datospos'  if db == None else db
DB_USER     = 'usuario2'  if usr == None else usr 
DB_PASSWORD = '123456789' if pwd == None else pwd 

TABLES = {}
PROCEDURES = {}

TABLES['rcpedidos'] = (
    """
    CREATE TABLE rcpedidos ( 
        rcp_cia varchar(10) NOT NULL , 
        rcp_pedido varchar(10) NOT NULL , 
        rcp_cliente varchar(25) NOT NULL , 
        rcp_fecha varchar(100) NOT NULL , 
        rcp_vendedor varchar(25) NOT NULL , 
        rcp_entregar varchar(25) NOT NULL , 
        rcp_status char(10) NOT NULL , 
        rcp_monto numeric(10,2) NOT NULL , 
        rcp_descuento numeric(10,2) NOT NULL , 
        usuario char(10) NOT NULL , 
        fecha_registro datetime NOT NULL , 
        hora_registro time NOT NULL , 
        rcp_abono numeric(10,2) NOT NULL , 
        rcp_tipo_venta varchar(2) NOT NULL , 
        rcp_comentario varchar(400) , 
        rcp_descto_porc numeric(5,2) , 
        rcp_descto_cod char(25) , 
        rcp_itbm numeric(6,2) , 
        rcp_dep_base numeric(6,2) , 
        rcp_hora_entrega time NOT NULL , 
        rcp_fecha_entrega VARCHAR(100) NOT NULL , 
        rcp_fecha_prod VARCHAR(100) NOT NULL , 
        rcp_anulado_por char(100) , 
        rcp_produccion numeric(2,0) , 
        rcp_documento varchar(25) , 
        rcp_chofer varchar(25) , 
        rcp_ruta varchar(25) , 
        rcp_salida varchar(25) , 
        rcp_impuesto1 numeric(7,2) , 
        rcp_impuesto2 numeric(7,2) , 
        rcp_impuesto3 numeric(7,2) , 
        rcp_impuesto4 numeric(7,2) , 
        rcp_impuesto5 numeric(7,2) , 
        rcp_imput1 varchar(25) , 
        rcp_imput2 varchar(25) , 
        rcp_imput3 varchar(25) , 
        rcp_imput4 varchar(25) , 
        rcp_imput5 varchar(25) , 
        rcp_entrega char(25)  ,
        PRIMARY KEY (rcp_cia, rcp_pedido) 
    ) 

    """
)

TABLES['rcpedidos1'] = TABLES['rcpedidos'].replace(' rcpedidos ', ' rcpedidos1 ') #copia para manejar la venta credito


TABLES['rdpedidos'] = (
    """
      CREATE TABLE rdpedidos (
        rdp_cia varchar(2) NOT NULL , 
        rdp_pedido varchar(10) NOT NULL , 
        rdp_linea numeric(4,0) NOT NULL , 
        rdp_producto varchar(5) NOT NULL , 
        rdp_cantidad numeric(5,0) NOT NULL , 
        rdp_precio numeric(7,2) , 
        rdp_monto numeric(7,2) , 
        rdp_comentario varchar(1000) , 
        rdp_departamento varchar(2) , 
        rdp_descto numeric(6,2) , 
        rdp_descto_porc numeric(5,2) , 
        rdp_descto_cod char(2) , 
        rdp_itbm numeric(6,2) , 
        rdp_entregado numeric(5,0) , 
        rdp_cod_kit varchar(5) , 
        rdp_itbms numeric(6,2) , 
      PRIMARY KEY (rdp_cia, rdp_pedido, rdp_linea)
      )    
    """ 
)

TABLES['rdpedidos1'] = TABLES['rdpedidos'].replace(' rdpedidos ', ' rdpedidos1 ')


TABLES['registro'] = (
    """
        CREATE TABLE registro (
            rcp_cia varchar(2) NOT NULL , 
            rcp_pedido varchar(10) NOT NULL ,
            reg_internalId int ,
            reg_resultado varchar(500) NOT NULL ,
            reg_estatus varchar(20) NOT NULL ,
            reg_grupo  varchar(100) ,
            reg_fecha_modificacion timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            reg_fecha_creacion timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ,
            PRIMARY KEY (rcp_cia, rcp_pedido)
            )
 
    """ 
    )


TABLES['equivalencias'] = (
    """
        CREATE TABLE equivalencias (
            id              int NOT NULL AUTO_INCREMENT PRIMARY KEY,  
            tabla           varchar(100) NOT NULL ,
            codigo_origen   varchar(100) NOT NULL ,
            codigo_destino  varchar(100) NOT NULL ,
            descripcion     varchar(300) NULL ,
            UNIQUE KEY (tabla, codigo_origen)
            )
 
    """ 
    )


TABLES['ns_items'] = (
    """
        CREATE TABLE ns_items (
            internalId          int NOT NULL ,
            nombre              varchar(100) NOT NULL ,
            tipo                varchar(100) NOT NULL ,
            cantidad            varchar(300)  ,
            unidad              varchar(100) ,
            ubicacion           varchar(300) ,
            precio              float ,
            fec_creac           timestamp ,
            fec_modif           timestamp ,
            lote                varchar(300) ,
            fec_caduc           timestamp  ,
            inactivo            varchar(100),
            item_pos            varchar(100),
            item_pos_group      int,
            item_pos_supply     int,
            codigo_barra        varchar(200),
            tipo_codigo_barra   varchar(200),
            codigo_impuesto     int,
            precio_alt1         float,
            precio_alt2         float,
            precio_alt3         float,
            precio_alt4         float
            )

    """
)

TABLES['ns_ordenes_cabecera'] = (
    """
        CREATE TABLE ns_ordenes_cabecera (
           num_documento        varchar(300) NOT NULL,
           num_transaccion      varchar(300) NOT NULL,
           fecha                timestamp,
           cliente_internalId   varchar(100),
           cliente_identific    varchar(300),
           fecha_creacion       timestamp,
           usuario              varchar(100),
           ubicacion            varchar(100),
           tipo                 varchar(100),
           importe_bruto        float,
           cod_descuento        varchar(100),
           importe_descuento    float,
           creador              varchar(100),
           fecha_creacion2      timestamp,
           abono                float,
           tipo_factura         varchar(300),
           nota                 varchar(1000),
           importe_neto         float,
           fecha_entrega        timestamp,
           hora_entrega         timestamp,
           estado               varchar(100),
           ruc                  varchar(100),
           dv                   varchar(100),
           nombre               varchar(300),
           email                varchar(100),
           id_tel               varchar(100),
           internalId           varchar(100) NOT NULL,
           impuesto             float,
           cant_lineas          int ,
           proc_status          varchar(10),
           proc_descr           varchar(10000)

            )

    """
)

TABLES['ns_ordenes_detalle'] = (
    """
        CREATE TABLE ns_ordenes_detalle (
           fecha                timestamp,
           cliente_internalId   varchar(100),
           num_documento        varchar(300) ,
           articulo_internalId  varchar(100) ,
           articulo_descr       varchar(100) ,
           cantidad             int,
           precio               float,
           importe_bruto        float,
           nota                 varchar(1000),
           dedicatoria          varchar(1000),
           ubicacion            varchar(100) ,
           impuesto             float ,
           linea                int
            )

    """
)


#------------------------  VISTAS ---------------------

TABLES ['vi_rcpedidos'] = (
   """
                    CREATE or REPLACE VIEW vi_rcpedidos AS    
                        select  
                             a.rcp_cia
                           , a.rcp_pedido
                           , (select codigo_destino from equivalencias e where e.tabla = 'clientes' and e.codigo_origen = a.rcp_cliente) rcp_cliente
                           , a.rcp_fecha
                           , a.rcp_status
                           , a.usuario
                           , a.fecha_registro
                           , a.hora_registro
                           , a.rcp_anulado_por
                           , a.rcp_comentario
                           , (select codigo_destino from equivalencias e where e.tabla = 'ubicaciones' and e.codigo_origen = 0 ) cod_ubicacion
                           , (select codigo_destino from equivalencias e where e.tabla = 'cuentas' and e.codigo_origen = '1110' ) num_cuenta
          
                           from rcpedidos a


   """ 
)


TABLES ['vi_rdpedidos'] = (
       """
                CREATE or REPLACE VIEW vi_rdpedidos AS 
                        select
                             a.rdp_cia
                           , a.rdp_pedido
                           , (select codigo_destino from equivalencias e where e.tabla = 'articulos' and e.codigo_origen = a.rdp_producto) rdp_producto
                           , a.rdp_linea
                           , a.rdp_precio
                           , a.rdp_comentario
					    from rdpedidos a
        """
        )

TABLES ['vi_venta_contado_pend'] = (
    """
                    CREATE or REPLACE view vi_venta_contado_pend AS    
                        select  a.*, b.reg_estatus, b.reg_fecha_modificacion, b.reg_resultado
                           from vi_rcpedidos a left join registro b 
                           on a.rcp_pedido = b.rcp_pedido 
                           where ifnull(b.reg_estatus,'NW') in ( 'NW', 'KO') 
                           
                           AND a.rcp_pedido in (
                                    select a.rdp_pedido from vi_rdpedidos a 
                                    where rdp_cia = '02'
                                    group by a.rdp_pedido
                                    having count(*) = count(a.rdp_producto)
                                )
                           order by rcp_cia, reg_fecha_modificacion asc, rcp_pedido   
    """
)

TABLES ['vi_ventas_pendientes'] = (
   """
            CREATE or REPLACE view vi_ventas_pendientes AS
                  select 
                             a.rcp_cia
                           , a.rcp_pedido
                           , a.rcp_cliente
                           , a.rcp_fecha
                           , a.rcp_status
                           , a.rcp_vendedor
                           , a.rcp_entregar
                           , a.fecha_registro
                           , a.hora_registro
                           , a.rcp_anulado_por
                           , a.rcp_comentario
                           , a.rcp_monto
                           , a.rcp_salida
                           , a.rcp_imput1
                           , a.rcp_imput2
                           , a.rcp_impuesto1
                           , a.rcp_impuesto2
                           , b.reg_estatus
                           , b.reg_fecha_modificacion 
                           , b.reg_resultado
                        
                           from rcpedidos a left join registro b 
                             on a.rcp_pedido = b.rcp_pedido 
                           where ifnull(b.reg_estatus,'NW') in ( 'NW') 
                           order by rcp_cia, reg_fecha_modificacion asc, rcp_pedido  
   """
)

TABLES ['vi_ordenes_cab'] = (
    """
    CREATE OR REPLACE VIEW vi_ordenes_cab AS

    SELECT    num_documento 
            , num_transaccion fecha
            , cliente_internalId
            , cliente_identific
            , DATE_FORMAT(fecha_creacion,'%Y-%m-%d') fecha_creacion
            , usuario
            , ubicacion
            , tipo
            , round(importe_bruto,2) importe_bruto
            , cod_descuento
            , round(importe_descuento,2) importe_descuento 
            , creador
            , DATE_FORMAT(fecha_creacion2,'%Y-%m-%d') fecha_creacion2
            , round(abono,2) abono
            , tipo_factura
            , nota
            , round(importe_neto,2) importe_neto 
            , DATE_FORMAT(fecha_entrega,'%Y-%m-%d') fecha_entrega
            , DATE_FORMAT(hora_entrega,'%H:%i') hora_entrega
            , estado
            , ruc
            , dv
            , nombre
            , email
            , id_tel 
        FROM ns_ordenes_cabecera

    """
)


TABLES ['vi_ordenes_det'] = (
    """
    CREATE OR REPLACE VIEW vi_ordenes_det AS
        SELECT DATE_FORMAT(fecha,'%Y-%m-%d') fecha
              , cliente_internalId
              , num_documento
              , articulo_internalId
              , articulo_descr
              , cantidad
              , round(precio, 2) precio
              , round(importe_bruto,2) importe_bruto
              , nota
              , dedicatoria
              , ubicacion 
        FROM ns_ordenes_detalle

    """
)

TABLES['vi_resumen_item_ant'] = (
    """
    CREATE OR REPLACE VIEW vi_resumen_item_ant AS
	SELECT 1 id,
         ( SELECT convert(codigo_destino, SIGNED INTEGER) from equivalencias WHERE tabla = 'ant.resumen_items' and codigo_origen = '_assembly' limit 1 )  ensamblado , 
         (SELECT convert(codigo_destino, SIGNED INTEGER) from equivalencias WHERE tabla = 'ant.resumen_items' and codigo_origen = '_inventoryItem' limit 1 ) terminado ,
         (SELECT convert(codigo_destino, SIGNED INTEGER) from equivalencias WHERE tabla = 'ant.resumen_items' and codigo_origen = '_kit' ) kit,
         (SELECT convert(codigo_destino, SIGNED INTEGER)  from equivalencias WHERE tabla = 'ant.total_items' and codigo_origen = 'cantidad' limit 1 )   cantidad,
         ( SELECT codigo_destino from equivalencias WHERE tabla = 'ant.fecproc_items' and codigo_origen = 'fecha' ) fecha
    """
)

TABLES['vi_resumen_item_act'] = (
    """
    CREATE OR REPLACE VIEW vi_resumen_item_act AS
        SELECT 1 id, 
           ( SELECT COUNT(*) FROM ns_items where tipo = '_assembly' ) ensamblado , 
           ( SELECT COUNT(*) FROM ns_items where tipo = '_inventoryItem') terminado ,
           (SELECT COUNT(*) FROM ns_items where tipo = '_kit' ) kit ,
           (SELECT COUNT(*) FROM ns_items ) cantidad,
           (select codigo_destino from equivalencias where tabla='act.fecproc_items' 
                   and codigo_origen = 'fecha' ) fecha    """
)


TABLES['vi_resumen_ordenes_act'] = (
 """
    CREATE OR REPLACE VIEW vi_resumen_ordenes_act AS
    select 1 id,
    (select count(*) from ns_ordenes_cabecera ) as cantidad,
    (select count(*) from ns_ordenes_detalle) as lineas, 
    (select count(distinct cliente_internalid) from ns_ordenes_cabecera) as clientes,
    (select count(distinct ubicacion) from ns_ordenes_cabecera ) as ubicaciones,
    (select sum(importe_bruto) from ns_ordenes_cabecera ) as monto  
    """  
)

#------- PROCEDIMIENTOS ---------

PROCEDURES['pa_registrar_items'] = (
    """
        DROP PROCEDURE IF EXISTS pa_registrar_items ;

        CREATE PROCEDURE pa_registrar_items (IN grupo VARCHAR(10) )
                Begin
                    delete from equivalencias where tabla in
                        ( concat(grupo,'.resumen_items'), concat(grupo,'.total_items'), concat(grupo,'.fecproc_items') ) ;

                    insert into equivalencias (tabla, codigo_origen, codigo_destino) 
                          select concat(grupo,'.resumen_items') nom , tipo, count(*)
                        from ns_items group by tipo 
                        union
                        select concat(grupo,'.total_items'), 'cantidad', count(*) 
                        from ns_items
                        union
                        select concat(grupo,'.fecproc_items'), 'fecha', LOCALTIME ;
                End ;


    """
)

#----------------------------------

config = {
    'user': DB_USER,
    'password': DB_PASSWORD,
    'host': DB_HOST,
    'database': DB_NAME,
    'raise_on_warnings': True
    }


def crear_bdatos():

    db_connection = mysql.connector.connect(
	    host= DB_HOST,
	    user= DB_USER,
	    passwd= DB_PASSWORD
    )

    # creating database_cursor to perform SQL operation
    cursor = db_connection.cursor()

    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8mb4'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database Creation: {}".format(err))
        exit(1)

def crear_tablas():
    cnx =  mysql.connector.connect(
	    host= DB_HOST,
	    user= DB_USER,
	    passwd= DB_PASSWORD
    )
    
    cursor = cnx.cursor(buffered=True) ##usamos buffer porque vamos a reutilizar el cursor y los resultados son minimos (solo un conteo) 

    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            crear_bdatos()
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)


    try:

        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print("Creating table/view {}: ".format(table_name), end='')
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")

        for proc_name in PROCEDURES:
            proc_description = PROCEDURES[proc_name]
            try:
                print("Creating procedure {}: ".format(proc_name), end='')
                cursor.execute(proc_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")

        cursor.close()


    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()

if __name__ == "__main__":
   crear_tablas()
