from __future__ import unicode_literals

import frappe
#from email_reply_parser import EmailReplyParser
#from markdown2 import markdown
import time

@frappe.whitelist()
def get_payments():
    payments = frappe.get_list('Payment Entry', filters={'docstatus': 0, 'payment_type': 'Pay'}, fields=['name', 'posting_date', 'paid_amount', 'party', 'paid_from'], order_by='posting_date')
    
    return { 'payments': payments }

@frappe.whitelist()
def generate_payment_file(payments):
    # creates a pain.001 payment file from the selected payments
    
    # convert string parameter into array
    payments = eval(payments)
    
    # create xml header
    content = get_line_string("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
    content += get_line_string("<Document xmlns=\"http://www.six-interbank-clearing.com/de/pain.001.001.03.ch.02.xsd\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://www.six-interbank-clearing.com/de/pain.001.001.03.ch.02.xsd  pain.001.001.03.ch.02.xsd\">")
    content += get_line_string("  <CstmrCdtTrfInitn>")
    # create group header
    content += get_line_string("      <GrpHdr>")
    # message ID
    content += get_line_string("        <MsgId>MSG-" + time.strftime("%Y%m%d%H%M%S") + "</MsgId>")
    # creation date and time ( e.g. 2010-02-15T07:30:00 )
    content += get_line_string("        <CreDtTm>" + time.strftime("%Y-%m-%dT%H:%M:%S") + "</CreDtTm>")
    # number of transactions
    content += get_line_string("        <NbOfTxs>{0}</NbOfTxs>".format(len(payments)))
    # total amount of all transactions ( e.g. 15850.00 )   
    content += get_line_string("        <CtrlSum>{0}</CtrlSum>".format(get_total_amount(payments)))
    content += get_line_string("        <InitgPty>")
    # company name ( e.g. MUSTER AG )
    content += get_line_string("          <Nm>{0}</Nm>".format(get_company_name(payments[0])))
    content += get_line_string("        </InitgPty>")
    content += get_line_string("      </GrpHdr>")

    for payment in payments:
        # create the payment entries
        content += get_line_string("      <PmtInf>")
        content += get_line_string("        <PmtInfId>{{ payment_info_id PMTINF-01 }}</PmtInfId>")
        content += get_line_string("        <PmtMtd>{{ payment_method TRF }}</PmtMtd>")
        content += get_line_string("        <BtchBookg>true</BtchBookg>")
        content += get_line_string("        <ReqdExctnDt>2010-02-22</ReqdExctnDt>")
        content += get_line_string("        <Dbtr>")
        content += get_line_string("          <Nm>MUSTER AG</Nm>")
        content += get_line_string("          <PstlAdr>")
        content += get_line_string("            <Ctry>CH</Ctry>")
        content += get_line_string("            <AdrLine>SELDWYLA</AdrLine>")
        content += get_line_string("          </PstlAdr>")
        content += get_line_string("        </Dbtr>")
        content += get_line_string("        <DbtrAcct>")
        content += get_line_string("          <Id>")
        content += get_line_string("            <IBAN>CH5481230000001998736</IBAN>")
        content += get_line_string("          </Id>")
        content += get_line_string("        </DbtrAcct>")
        content += get_line_string("        <DbtrAgt>")
        content += get_line_string("          <FinInstnId>")
        content += get_line_string("            <BIC>RAIFCH22</BIC>")
        content += get_line_string("          </FinInstnId>")
        content += get_line_string("        </DbtrAgt>")
        content += get_line_string("        <CdtTrfTxInf>")
        content += get_line_string("          <PmtId>")
        content += get_line_string("            <InstrId>INSTRID-01-01</InstrId>")
        content += get_line_string("            <EndToEndId>ENDTOENDID-001</EndToEndId>")
        content += get_line_string("          </PmtId>")
        content += get_line_string("          <PmtTpInf>")
        content += get_line_string("            <LclInstrm>")
        content += get_line_string("              <Prtry>CH01</Prtry>")
        content += get_line_string("            </LclInstrm>")
        content += get_line_string("          </PmtTpInf>")
        content += get_line_string("          <Amt>")
        content += get_line_string("            <InstdAmt Ccy=\"CHF\">3949.75</InstdAmt>")
        content += get_line_string("          </Amt>")
        content += get_line_string("          <CdtrAcct>")
        content += get_line_string("            <Id>")
        content += get_line_string("              <Othr>")
        content += get_line_string("                <Id>01-39139-1</Id>")
        content += get_line_string("              </Othr>")
        content += get_line_string("            </Id>")
        content += get_line_string("          </CdtrAcct>")
        content += get_line_string("          <RmtInf>")
        content += get_line_string("            <Strd>")
        content += get_line_string("              <CdtrRefInf>")
        content += get_line_string("                <Ref>210000000003139471430009017</Ref>")
        content += get_line_string("              </CdtrRefInf>")
        content += get_line_string("            </Strd>")
        content += get_line_string("          </RmtInf>")
        content += get_line_string("        </CdtTrfTxInf>")
        content += get_line_string("      </PmtInf>")
    # add footer
    content += get_line_string("  </CstmrCdtTrfInitn>")
    content += get_line_string("</Document>")
    
    return { 'content': content }

def get_total_amount(payments):
    # get total amount from all payments
    total_amount = float(0)
    for payment in payments:
        payment_amount = frappe.get_value('Payment Entry', payment, 'paid_amount')
        if payment_amount:
            total_amount += payment_amount
        
    return total_amount

def get_company_name(payment_entry):
    return frappe.get_value('Payment Entry', payment_entry, 'company')

# create a line (with windows-compatible line ending)    
def get_line_string(line):
    return "{0}\r\n".format(line)
