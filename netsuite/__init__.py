

from netsuite.client import  NetSuiteClient
from netsuite.credenciales import Credentials, Signature
from netsuite.utilidades import grabarEntradaXML, grabarSalidaXML
from netsuite.commands import  searchAccount, upsertRecord, itemSearch , itemCustomSearch, getSavedSearch, Search, SearchMore

#clases construidas manualmente y que no usan el la creación de tipos de zeep
from netsuite.t_cash_sale import CashSaleHeader
from netsuite.t_customers import CustomerHeader
from netsuite.commands import UpsertHeader
