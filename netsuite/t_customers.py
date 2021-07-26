import xml.etree.ElementTree as xml

#ejemplo tomado del manual donde se ve la estructura de un cliente
texto = """
 <soap:Body>
   <upsert xmlns="urn:messages_2017_1.platform.webservices.netsuite.com">
     <record xmlns:q1="urn:relationships_2017_1.lists.webservices.netsuite.com" xsi:type="q1:Customer" externalId="THISISMYEXTID">
       <q1:entityId>XYZ 2 Inc</q1:entityId>
       <q1:companyName>XYZ 2, Inc.</q1:companyName>
       <q1:email>bsanders@xyz.com</q1:email>
     </record>
   </upsert>
 </soap:Body>
"""

class CustomerHeader():
    # Esta clase construye manualmente el registro xml para un cliente
    def __init__(self, elemento, **kwargs):

      # Preparamos un registro.  Se asume que la cabecera tendra una propiedad function
      self.record = xml.SubElement(elemento,'record')
      self.record.set('xmlns:q1','urn:relationships_2020_2.lists.webservices.netsuite.com')
      self.record.set('xsi:type','q1:Customer')
      self.record.set('externalId',kwargs.get('ID'))

      self.entiyId = xml.SubElement(self.record, 'q1:entityId')
      self.entiyId.text  = kwargs.get('ID')
 
      self.companyName = xml.SubElement(self.record, 'q1:companyName')
      self.companyName.text  = kwargs.get('COMPANY')

      self.eMail = xml.SubElement(self.record, 'q1:email')
      self.eMail.text  = kwargs.get('EMAIL')


       

if __name__ == "__main__":

   pass
