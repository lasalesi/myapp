from __future__ import unicode_literals

import frappe
from email_reply_parser import EmailReplyParser
from markdown2 import markdown

@frappe.whitelist()
def parse_file(content):
	# content is the plain text content, parse 
	frappe.throw("Got a file!" + content)

	return
