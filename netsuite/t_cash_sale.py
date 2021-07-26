import xml.etree.ElementTree as xml
from io import BytesIO

class CashSaleHeader():
    
    def __init__(self, elemento, **kwargs):

       # Esta clase construye manualmente el registro xml para una venta al contado TODO: AUN SIN IMPLEMENTAR.  EL CODIGO ES DE CLIENTE
        self.record = xml.SubElement(elemento, 'record')
        self.record.set('xmlns:q1','urn:sales_2020_1.transactions.webservices.netsuite.com')
        self.record.set('xsi:type','q1:CashSale')
        self.record.set('externalId',kwargs.get('ID'))

        self.entiyId = xml.SubElement(self.record, 'q1:entityId')
        self.entiyId.text  = kwargs.get('ID')

        self.companyName = xml.SubElement(self.record, 'q1:companyName')
        self.companyName.text  = kwargs.get('COMPANY')

        self.eMail = xml.SubElement(self.record, 'q1:email')
        self.eMail.text  = kwargs.get('EMAIL')
   

if __name__ == "__main__":

   pass
