# -*- coding: utf-8 -*-
# Copyright (c) 2018, lasalesi and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import datetime

class SalesReport(Document):       
    def onload(self):
        pass

    def setup(self):
        pass
              
    def refresh(self):
        pass
        
    """ This function is called in a script fashion to populate the report 
        It can be executed from the wrapper
            myapp.myapp.doctype.sales_report.sales_report.create_report()
    """
    def fill(self):
        # prepare global variables
        today = datetime.now()
        self.date = today.strftime("%Y-%m-%d")
        self.week = today.strftime("%W")
        _week = int(today.strftime("%W"))
        
        # define each line item
        _description = "Octocat-" + today.strftime("%W")
        _sql_7days = """SELECT (IFNULL(SUM(`qty`), 0)) AS `qty`, 
                (IFNULL(SUM(`net_amount`), 0)) AS `revenue`
            FROM `tabDelivery Note Item`
            WHERE `item_code` LIKE 'Octocat'
            AND `docstatus` = 1
            AND `creation` > DATE_SUB(NOW(), INTERVAL 7 DAY)
            """
        _qty_7days,_revenue_7days = get_qty_revenue(_sql_7days)
        _sql_YTD = """SELECT (IFNULL(SUM(`qty`), 0)) AS `qty`, 
                (IFNULL(SUM(`net_amount`), 0)) AS `revenue`
            FROM `tabDelivery Note Item`
            WHERE `item_code` LIKE 'Octocat'
            AND `docstatus` = 1
            AND `creation` >= '{0}-01-01'
            """.format(today.strftime("%Y"))
        _qty_YTD,_revenue_YTD = get_qty_revenue(_sql_YTD)
        _sql_PY = """SELECT (IFNULL(SUM(`qty`), 0)) AS `qty`, 
                (IFNULL(SUM(`net_amount`), 0)) AS `revenue`
            FROM `tabDelivery Note Item`
            WHERE `item_code` LIKE 'Octocat'
            AND `docstatus` = 1
            AND `creation` >= '{0}-01-01'
            AND `creation` <= '{0}-12-31'
            """.format(int(today.strftime("%Y")) - 1)
        _qty_PY,_revenue_PY = get_qty_revenue(_sql_PY)
                        
        self.append('items', 
            { 
                'description': _description, 
                'qty_7days': _qty_7days,
                'revenue_7days': _revenue_7days,
                'qty_ytd': _qty_YTD,
                'revenue_ytd': _revenue_YTD, 
                'qty_py': _qty_PY,
                'revenue_py': _revenue_PY,
                'demand_qty_ytd': (_qty_YTD/_week),
                'demand_revenue_ytd': (_revenue_YTD/_week),
                'demand_qty_py': (_qty_PY/52), 
                'demand_revenue_py': (_revenue_PY/52)
            })

@frappe.whitelist()
def create_report():
    new_report = frappe.get_doc({"doctype": "Sales Report"})
    new_report.fill()
    new_report_name = new_report.insert()        
    return new_report

""" Extracts `result` from SQL query """
def get_value(sql):
    values = frappe.db.sql(sql, as_dict=True)
    return values[0].result

""" Extracts `qty` and `revenue` from SQL query """
def get_qty_revenue(sql):
    values = frappe.db.sql(sql, as_dict=True)
    return values[0].qty, values[0].revenue
