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
        _this_year = int(today.strftime("%Y"))
        _last_year = _this_year - 1
        self.this_year = _this_year
        self.last_year = _last_year
        
        # define each line item
        _description = "Octocat"
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
        
        # compute totals
        _total_qty_7days = 0
        _total_qty_ytd = 0 
        _total_demand_qty_ytd = 0
        _total_demand_qty_py = 0
        _total_qty_py = 0
        _total_revenue_7days = 0
        _total_revenue_ytd = 0
        _total_demand_revenue_ytd = 0
        _total_demand_revenue_py = 0
        _total_revenue_py = 0
        for item in doc.items:
            _total_qty_7days = _total_qty_7days + item.qty_7days
            _total_qty_ytd = _total_qty_ytd + item.qty_ytd
            _total_demand_qty_ytd = _total_demand_qty_ytd + item.demand_qty_ytd
            _total_demand_qty_py = _total_demand_qty_py + item.demand_qty_py
            _total_qty_py = _total_qty_py + item.qty_py
            _total_revenue_7days = _total_revenue_7days + item.revenue_7days
            _total_revenue_ytd = _total_revenue_ytd + item.revenue_ytd
            _total_demand_revenue_ytd = _total_demand_revenue_ytd + item.demand_revenue_ytd
            _total_demand_revenue_py = _total_demand_revenue_py + item.demand_revenue_py
            _total_revenue_py = _total_revenue_py + item.revenue_py
        
        self.total_qty_7days = _total_qty_7days
        self.total_qty_ytd = _total_qty_ytd 
        self.total_demand_qty_ytd = _total_demand_qty_ytd
        self.total_demand_qty_py = _total_demand_qty_py
        self.total_qty_py = _total_qty_py
        self.total_revenue_7days = _total_revenue_7days
        self.total_revenue_ytd = _total_revenue_ytd
        self.total_demand_revenue_ytd = _total_demand_revenue_ytd
        self.total_demand_revenue_py = _total_demand_revenue_py
        self.total_revenue_py = _total_revenue_py
        
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
