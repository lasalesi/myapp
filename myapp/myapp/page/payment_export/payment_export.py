from __future__ import unicode_literals

import frappe
#from email_reply_parser import EmailReplyParser
#from markdown2 import markdown

@frappe.whitelist()
def get_payments():
    payments = [ "PE-00003", "PE-00004" ]
    
    return { 'payments': payments }
