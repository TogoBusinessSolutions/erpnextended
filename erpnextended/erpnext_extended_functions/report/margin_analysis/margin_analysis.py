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
                        'fieldname': 'doc_type',
                        'fieldtype': 'data',
                        'label': 'Transaction Type'
                },
                {
                        'fieldname': 'item_cost',
                        'fieldtype': 'Float',
                        'label': 'Total Cost'
                },
        ]

        data = frappe.db.sql('''
            SELECT     
                tsi.name,tsi.creation,tsi.grand_total,tsi.territory,'Sales Invoice' as transaction_type,
                SUM(CASE tsii.item_code
                    WHEN 'NS-TRANS' THEN tsii.amount
                    ELSE tip.price_list_rate * (1 + IFNULL(tit.tax_rate,0)/100)
                END) as 'item_cost'
            FROM 
                `tabSales Invoice` tsi
            LEFT OUTER JOIN
                `tabSales Invoice Item` tsii on tsi.name = tsii.parent
            LEFT OUTER JOIN
                `tabItem` ti on ti.name = tsii.item_code 
            LEFT OUTER JOIN
                `tabItem Price` tip on tip.item_code = ti.name
	    LEFT OUTER JOIN 
		`tabItem Tax` tit on tit.parent = ti.name
            WHERE 
                tsi.docstatus = 1 AND tsi.creation between %s and %s AND tip.price_list = 'Standard Buying'
            GROUP BY
                tsi.name,tsi.creation,tsi.grand_total,tsi.territory,transaction_type
            UNION ALL
            SELECT     
                tsi.name,tsi.creation,tsi.grand_total,tsi.territory,'Sales Order' as transaction_type,
                SUM(CASE tsii.item_code
                    WHEN 'NS-TRANS' THEN tsii.amount
                    ELSE tip.price_list_rate * (1 + IFNULL(tit.tax_rate,0)/100 )
                END) as 'item_cost'
            FROM 
                `tabSales Order` tsi
            LEFT OUTER JOIN
                `tabSales Order Item` tsii on tsi.name = tsii.parent
            LEFT OUTER JOIN
                `tabItem` ti on ti.name = tsii.item_code 
            LEFT OUTER JOIN
                `tabItem Price` tip on tip.item_code = ti.name
            LEFT OUTER JOIN 
                `tabItem Tax` tit on tit.parent = ti.name
	    WHERE 
                tsi.docstatus = 1 AND tsi.creation between %s and %s AND tip.price_list = 'Standard Buying' and tsi.status <> 'Completed'
            GROUP BY
                tsi.name,tsi.creation,tsi.grand_total,tsi.territory,transaction_type
                 ''', (filters.from_date, filters.to_date,filters.from_date, filters.to_date))

        return columns, data
