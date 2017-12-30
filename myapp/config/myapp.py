from __future__ import unicode_literals
from frappe import _

def get_data():
    return[
        {
            "label": _("Records"),
            "icon": "fa fa-star",
            "items": [
                {
                    "type": "doctype",
                    "name": "Person",
                    "description": _("List of persons")
                },
		{
		    "type": "doctype",
                    "name": "Log",
                    "description": _("Log entries")
                }
            ]
        },
        {
            "label": _("Tools"),
            "icon": "fa fa-wrench",
            "items": [
                   {
                       "type": "page",
                       "name": "visual",
                       "label": "Visual",
                       "description": _("Visualisation")
                   },
                   {
                       "type": "page",
                       "name": "myimport",
                       "label": "MyImport",
                       "description": _("MyImport")
                   },
                   {
                       "type": "page",
                       "name": "mycalc",
                       "label": "MyCalc",
                       "description": _("MyCalc")
                   }
            ]
        }, 
        {
            "label": _("Banking"),
            "icon": "fa fa-money",
            "items": [
                   {
                       "type": "page",
                       "name": "bankimport",
                       "label": "Bank Import",
                       "description": _("Bank import")
                   },
                                      {
                       "type": "page",
                       "name": "payment_export",
                       "label": "Payment export",
                       "description": _("Payment export")
                   }
            ]
        } 
    ]
