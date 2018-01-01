#
# swiss_exchange_rates.py
#
# Copyright (C) libracore, 2017
# https://www.libracore.com or https://github.com/libracore
#
# For information on ERPNext, refer to https://erpnext.org/
#
# Execute with $ bench execute myapp.myapp.scripts.swiss_exchange_rates.py
#
from urllib.request import urlopen
import xml.etree.ElementTree as ET
import frappe

# import content into a string from URL XML data
# in Python 3, use urllib.request
url = "http://www.afd.admin.ch/publicdb/newdb/mwst_kurse/estv/mittelkurse_xml.php"
html = urlopen(url)
data = html.read()
html.close()

# parse string to an XML object
# Refer to https://docs.python.org/2/library/xml.etree.elementtree.html
root = ET.fromstring(data)
# debug
# for child in root:
#     print(child.tag, child.attrib)
# Note: xml uses an xsl template
for currency in root.findall('{http://www.afd.admin.ch/publicdb/newdb/mwst_mittelkurse}devise'):
    name = currency.find('{http://www.afd.admin.ch/publicdb/newdb/mwst_mittelkurse}waehrung')
    if "EUR" in name.text:
        rate = currency.find('{http://www.afd.admin.ch/publicdb/newdb/mwst_mittelkurse}kurs')
        print(name.text + " = " + rate.text + " CHF")

        # insert a new record in ERPNext
        new_exchange_rate = frappe.get_doc({"doctype": "Currency Exchange"})
        new_exchange_rate.date = strftime("%Y-%m-%d")
        new_exchange_rate.from_currency = "EUR"
        new_exchange_rate.to_currency = "CHF"
        # Exchange Rate (1 EUR = [?] CHF)
        new_exchange_rate.exchange_rate = rate
	new_exchange_rate.insert()