# -*- coding: utf-8 -*-
# Copyright (c) 2018, lasalesi and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import pdfkit, os, frappe
from frappe.model.document import Document

class MyLabel(Document):
	pass
	
def create_pdf(label):
	# create temporary file
	fname = os.path.join("/tmp", "frappe-pdf-{0}.pdf".format(frappe.generate_hash()))
	
	html = label.html
	options = { 
		'page-width': '{0}mm'.format(label.page_width), 
		'page-height': '{0}mm'.format(label.page_height), 
		'margin-top': '0mm',
		'margin-bottom': '0mm',
		'margin-left': '0mm',
		'margin-right': '0mm' }

	pdfkit.from_string(html, fname, options=options or {})
	
	with open(fname, "rb") as fileobj:
		filedata = fileobj.read()
		
	return filedata


@frappe.whitelist()
def download_mylabel(name):
	label = frappe.get_doc("MyLabel", name)
	frappe.local.response.filename = "{name}.pdf".format(name=name.replace(" ", "-").replace("/", "-"))
	frappe.local.response.filecontent = create_pdf(label)
	frappe.local.response.type = "download"
