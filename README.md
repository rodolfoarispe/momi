### SISTEMA DE INTEGRACION MOMI - NETSUITE
# Programa para la integración de informacion de ventas provenientes de los POS y que son enviados via el API de Netsuite a la instancia de Momi en la nube.

## Descripción
El sistema está compuesto de un packete (netsuite) responsable de establecer una conexión coherente con netsuite desde un punto común.  Las entidades a transferir así como la adecuación de sus campos antes de la trasnferencia se realiza en un paquete separado (momi)

El proceso de transferenecia de cada una las transacciones se estructuró en 4 archivos que atienden de manera individual los temas funcionales relacionados al proceso.  Esto con el fin de lograr mayor claridad del código:

- bucle de transferencia (xxx_buc.py)
- lectura desde la fuente (xxx_get.py)
- grabación en el destino (xxx_put.py)
- registro del resultado de la operación (xxx_reg.py)


## Paquete momi:
En este paquete es responsable de homologar las clases entre ambos sistemas y por tanto es capaz de tomar la estructura fuente y prepararla para ser enviadas a Netsuite (equivalencias). En el caso de la venta en efectivo por ejemplo, se define una clase cabecera y otra clase detalle y se incluyen los campos de interés necesarios para lograr una transferencia exitosa.

## Paquete netsuite:
Este paquete ha sido dividido en areas funcionales:
- client.py:  define una clase global NetSuiteClient que contiene el cliente HTTP y un generador de tokens
- commands.py: define las rutinas según las funciones API de netsuite, como por ejemplo upsert y search
- credenciales.py:  define una clase comun Credenciales donde están predefinidos los valores necesarios para generar las conexiones mediante Token Based Authentication (TBA)
- utilidades.py: rutinas genericas que realizan funciones de servicio al resto de los modulos

## Requerimientos técnicos:
Python 3.9


ORDEN DE VENTA:
IMPUT5 = ID ORDEN DE VENTA
IMPUT4 = ID DEL CIENTE DE NS (JORGE LO PONE AQUI)


Campos que dependen del InternalId del sandbox y que el POS tiene que manejar:

- Ubicación
- Usuario 
- Cliente Venta Contado
- Forma de Pago
- Vendedor
- Codigo de Articulo
- Codigo de Descuento y Tasa

Campos Custom que son requeridos por la interface:

VENTA CONTADO (CashSale):
- custbody_ad_dn_option_payment (metodo de pago1)
- custbody_ad_dm_payment_amount_1 (metodo de pago2)
- custbodyad_dm_payment_amount_2 (monto de pago2)

ITEMS (vienen en la consulta customsearch_ad_items_pos):
- custitem_ad_item_pos
- custitem_ad_item_group_pos 
- custitem_ad_item_supply_group
- custitem_ad_item_internal_upccode

SALES ORDER - DETALLE (viene en la consulta guardada customsearch_ad_dm_sales_order_details_2):
- custcol_ad_dm_dedication

SALES ORDER - CABECERA (vienen en la consulta guardada customsearch_ad_dm_sales_order):
- custbody_ad_pa_identification
- custbody_adc_usuario
- custbody_ad_pa_store
- custbody_ad_dm_date_delivery
- custbody_ad_pa_delivery_time
- custentity_ad_pa_id_number
- custentity_ad_pa_control_digits


Lista de Tareas:
- Menu de tareas manuales - rodolfo
- Prueba de descarga por demanda y automática
- Check de dependencias - rodolfo - jorge
- pruebas venta credito - rodolfo - jorge

OJO: 
- hay que trabajar en la tabla de flags para que ambos sistemas (interface y pos sepan cuando están trabajando y cuando estan en reposo)
- marcado de ordenes cuyo articulo no existe. Tentativo revisar si es posible forzar la actualizaciónde articulos o en su defecto, solo de aquellos que no se encontraron (a partir de su id) mediante un proceso adicional 
- Verificar como hacer que un trigger de sql dispare una sentencia en el shell.  Ejem https://stackoverflow.com/questions/33170615/call-python-script-from-mysql-trigger 


