# Copyright (c) 2013, Togo Business Solutions and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns = [
                {
                        'fieldname': 'posting_date',
                        'label': 'Date',
                        'fieldtype': 'Date'
                },
                {
                        'fieldname': 'amount',
                        'fieldtype': 'Float',
                        'label': 'Amount'
                },
                {
                        'fieldname': 'full_name',
                        'fieldtype': 'data',
                        'label': 'Journal'
                }
        ]

	data = frappe.db.sql('''select date(je.posting_date) as posting_date,
                je.total_debit as amount, je.name as name
                from `tabJournal Entry` je
                where date(je.posting_date) between %s and %s
                and je.docstatus = 1
		and je.name not in (select journal_entry from `tabEmployee Payment` where docstatus=1)
		and je.name in 
		(select parent from `tabJournal Entry Account` where debit > 0 and account in 
		(select allowed_account from `tabEmployee Payment Allowed Accounts`)) 
                 ''', (filters.from_date, filters.to_date))

        return columns, data
