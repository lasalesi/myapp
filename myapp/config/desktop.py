# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "MyApp",
			"color": "red",
			"icon": "octicon octicon-flame",
			"type": "module",
			"label": _("MyApp")
		}
	]
