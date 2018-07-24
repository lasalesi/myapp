# -*- coding: utf-8 -*-
# Copyright (c) 2018, libracore GmbH and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import math
from frappe import _
from datetime import datetime, timedelta

def create_sales_order():
    new_so = frappe.get_doc({
        "doctype": "Sales Order",
        "customer": "Guest",
        "items": [
            {
                "item_code": "Test",
                "qty": 1,
                "rate": 15
            }
        ],
        "delivery_date": (datetime.now() + timedelta(days=5))
    })
    new_so.insert()
    return

