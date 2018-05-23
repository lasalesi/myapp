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
                },
                {
                    "type": "doctype",
                    "name": "MyLabel",
                    "description": _("Create labels")
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
            "label": _("DocType Reports"),
            "icon": "fa fa-wrench",
            "items": [
                   {
                       "type": "doctype",
                       "name": "Sales Report",
                       "label": _("Sales Report"),
                       "description": _("Sales Report")
                   }
            ]
        }
    ]
