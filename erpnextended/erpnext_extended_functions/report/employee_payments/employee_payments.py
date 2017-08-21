# Copyright (c) 2013, Togo Business Solutions and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns = [
		{
			'fieldname': 'start_date',
			'label': 'Start Date',
			'fieldtype': 'Date'
		},
		{
                        'fieldname': 'end_date',
                        'label': 'End Date',
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
                        'label': 'Employee:200'
                },
		{
                        'fieldname': 'payment_type',
                        'fieldtype': 'data',
                        'label': 'Payment Type'
                }
	]

	data = frappe.db.sql('''select min(date(ep.posting_date)) as start_date,
		max(date(ep.posting_date)) as end_date,
		sum(epa.amount) as amount, epa.full_name,epa.payment_type
		from `tabEmployee Payment` ep inner join
		`tabEmployee Payment Allocation` epa 
		on ep.name = epa.parent
			where (date(ep.posting_date) between %s and %s)
			and ep.docstatus = 1
		group by epa.full_name,epa.payment_type
		 ''', (filters.from_date, filters.to_date))

	return columns, data
