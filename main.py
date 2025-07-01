# Sample Flask API (Simulated Third-Party Service)
from flask import Flask, request, Response
import xml.etree.ElementTree as ET
import requests
from lxml import etree

app = Flask(__name__)

@app.route('/pay', methods=['POST'])
def pay():
    try:
        xml_data = request.data
        root = ET.fromstring(xml_data)

        customer_id = root.findtext('CustomerID')
        amount = root.findtext('Amount')
        biller_code = root.findtext('BillerCode')
        ref = root.findtext('PaymentReference')

        # Mock validation and success response
        response_xml = f'''
        <BillPaymentResponse>
            <Status>Success</Status>
            <ReferenceID>{ref}</ReferenceID>
            <Message>Payment processed successfully.</Message>
        </BillPaymentResponse>
        '''
        return Response(response_xml, mimetype='application/xml')
    except Exception as e:
        error_xml = f'<Error><Message>{str(e)}</Message></Error>'
        return Response(error_xml, status=500, mimetype='application/xml')

if __name__ == '__main__':
    app.run(debug=True, port=5000)


# -----------------------------
# XML Client (Request Sender)
# -----------------------------
def send_xml_request():
    url = 'http://localhost:5000/pay'
    headers = {'Content-Type': 'application/xml'}

    xml_request = '''
    <BillPaymentRequest>
        <CustomerID>99881234</CustomerID>
        <Amount>3500</Amount>
        <BillerCode>PHCN01</BillerCode>
        <PaymentReference>ABC12345678</PaymentReference>
    </BillPaymentRequest>
    '''

    # Optional XSD Validation
    try:
        with open('bill_payment.xsd', 'rb') as f:
            schema_root = etree.XML(f.read())
            schema = etree.XMLSchema(schema_root)
            doc = etree.fromstring(xml_request.encode())
            schema.assertValid(doc)
    except Exception as e:
        print(f'XSD validation failed: {e}')
        return

    response = requests.post(url, data=xml_request, headers=headers)
    print('--- Response ---')
    print(response.text)


# -----------------------------
# Dummy XSD File (bill_payment.xsd)
# -----------------------------
# Save this content as 'bill_payment.xsd' in the same directory
'''
<?xml version="1.0"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="BillPaymentRequest">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="CustomerID" type="xs:string"/>
        <xs:element name="Amount" type="xs:decimal"/>
        <xs:element name="BillerCode" type="xs:string"/>
        <xs:element name="PaymentReference" type="xs:string"/>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
'''

# Run this
if __name__ == '__main__':
    # app.run(debug=True, port=5000)  # comment this line
    send_xml_request()

