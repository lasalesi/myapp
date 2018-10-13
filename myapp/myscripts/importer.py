# -*- coding: utf-8 -*-
# Copyright (c) 2017-2018, libracore and contributors
# License: AGPL v3. See LICENCE
#
# Run with:
#   $ bench execute myapp.myscripts.importer.get_bo_descriptions --args "['/home/frappe/files/']"

from __future__ import unicode_literals
import frappe
from frappe import throw, _
from bs4 import BeautifulSoup
import os

def get_bo_descriptions(path):
    
    for filename in os.listdir(path):
        soup = BeautifulSoup(open(path + filename), 'lxml')
        customer_name = soup.customer_name.get_text()
        description = soup.decription.get_text()
        
        print(customer_name)
        #print(description)
        customers = frappe.get_all("Customer", filters={'customer_name': customer_name}, fields=['name'])
        if customers:
            customer = frappe.get_doc("Customer", customers[0]['name'])
            customer.customer_details = description
            customer.save()
            frappe.db.commit()
        else:
            frappe.log_error("Customer {0} from file {1} not found.".format(customer_name, filename))
        #print(soup)
