# Copyright (c) 2013, Togo Business Solutions and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns = [
		{
                        'fieldname': 'name',
                        'fieldtype': 'data',
                        'label': 'Document'
                },
                {
                        'fieldname': 'creation',
                        'label': 'Date Created',
                        'fieldtype': 'Date'
                },
		        {
                        'fieldname': 'total',
                        'fieldtype': 'Float',
                        'label': 'Total'
                },
                {
                        'fieldname': 'grand_total',
                        'fieldtype': 'Float',
                        'label': 'Grand Total'
                },
                {
                        'fieldname': 'territory',
                        'label': 'Territory',
                        'fieldtype': 'data'
                },
                {
                        'fieldname': 'sales_person',
                        'label': 'Sales Person',
                        'fieldtype': 'data'
                },
                {
                        'fieldname': 'doc_type',
                        'fieldtype': 'data',
                        'label': 'Transaction Type'
                },
        ]

        data = frappe.db.sql('''
            SELECT     
                tsi.name as name,tsi.creation as creation,tsi.total as total,tsi.grand_total as grand_total,
                tsi.territory,tsp.sales_person,'Sales Invoice' as doc_type
            FROM 
                `tabSales Invoice` tsi
            LEFT OUTER JOIN
                `tabSales Team` tsp on tsi.name = tsp.parent
            WHERE 
                tsi.docstatus = 1 AND tsi.creation between %s and %s
            UNION ALL
            SELECT     
                tso.name,tso.creation,tso.total,tso.grand_total,tso.territory,tsp.sales_person,'Sales Order' as doc_type
            FROM 
                `tabSales Order` tso
            LEFT OUTER JOIN
                `tabSales Team` tsp on tso.name = tsp.parent
            WHERE 
                tso.docstatus = 1 AND tso.creation between %s and %s and tso.status <> 'Completed'
                 ''', (filters.from_date, filters.to_date,filters.from_date, filters.to_date))

        return columns, data
