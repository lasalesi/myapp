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
                }
            ]
        }
    ]