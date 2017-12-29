from __future__ import unicode_literals

import frappe
from email_reply_parser import EmailReplyParser
from markdown2 import markdown

def parse(content):
    # this parses the content
    lines = content.split("\n")
    for line in lines:
        fields = line.split("\t")
        for field in fields:
            print("Field: " + field)
            
    return

def parse_ubs(content):
    # parse a ubs bank extract csv
    # collect all lines of the file
    log("Starting parser...")
    lines = content.split("\n")
    for i in range(1, len(lines)):
        log("Reading {0} of {1} lines...".format(i, len(lines)))
        # skip line 0, it contains the column headers
        # collect each fields (separated by semicolon)
        fields = lines[i].split(';')

        # collect created payment entries
        new_payment_entries = []
        
        # get received amount, only continue if this has a value
        received_amount = fields[19]
        log("Received amount {0} ({1}, {2})".format(received_amount, fields[18], fields[20]))
        if received_amount != "":
            # get unique transaction ID
            transaction_id = fields[15]
            log("Checking transaction {0}".format(transaction_id))
            # cross-check if this transaction was already recorded
            if not frappe.db.exists('Payment Entry', {'reference_no': transaction_id}):
                log("Adding transaction {0}".format(transaction_id))
                # create new payment entry
                new_payment_entry = frappe.get_doc({'doctype': 'Payment Entry'})
                new_payment_entry.naming_series = "PE-"
                new_payment_entry.payment_type = "Receive"
                # date is in DD.MM.YYYY
                date_parts = fields[11].split('.')
                date = date_parts[2] + "-" + date_parts[1] + "-" + date_parts[0]
                new_payment_entry.posting_date =  date
                # new_payment_entry.paid_to 
                # new_payment_entry.paid_to_account_currency
                new_payment_entry.paid_amount = received_amount
                new_payment_entry.reference_no = transaction_id
                new_payment_entry.reference_date = date
                inserted_payment_entry = new_payment_entry.insert()
                new_payment_entries.append(inserted_payment_entry.name)
            
	return new_payment_entries

def log(comment):
	new_comment = frappe.get_doc({"doctype": "Log"})
	new_comment.comment = comment
	new_comment.insert()
	return new_comment
	        
@frappe.whitelist()
def parse_file(content, bank="ubs"):
    # content is the plain text content, parse 
    # frappe.throw("Got a file!" + content)
    if bank == "ubs":
        new_records = parse_ubs(content)
        
    return { "message": "Done", "records": new_records }

