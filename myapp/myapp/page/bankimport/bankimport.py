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
    
    return
    
@frappe.whitelist()
def parse_file(content, bank="ubs"):
    # content is the plain text content, parse 
    # frappe.throw("Got a file!" + content)
    if bank == "ubs":
        parse_ubs(content)
        
    return { "message": "Done" }

