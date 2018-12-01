# Copyright (c) 2013, Togo Business Solutions and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns = [
		{
                        'fieldname': 'Sales_Person',
                        'fieldtype': 'data',
                        'label': 'Sales Person'
                },
		{
                        'fieldname': 'amount',
                        'fieldtype': 'Float',
                        'label': 'Amount'
                },
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
                        'fieldname': 'Account',
                        'fieldtype': 'data',
                        'label': 'Branch'
                },
        ]

        data = frappe.db.sql('''SELECT
		tst2.sales_person as 'Sales_Person', 
		SUM(tpe.paid_amount) as 'Amount',
		MIN(tpe.posting_date) as 'Start_date',
		MAX(tpe.posting_date) as 'End_Date',
		sa1.branch as Account
		FROM 
			`tabPayment Entry` tpe
		LEFT OUTER JOIN
			`tabPayment Entry Reference` ter
		ON
			tpe.name=ter.parent
		LEFT OUTER JOIN
			`tabSales Team` tst2 
		ON
			tst2.parent=ter.reference_name
		LEFT OUTER JOIN
			`tabSales Accounts` sa1
		ON
			sa1.account = tpe.paid_to
		WHERE
			tpe.posting_date between %s and %s
		AND 
			tpe.docstatus=1
		AND
			tpe.payment_type='Receive'
		AND tpe.paid_to in (SELECT sa2.account from `tabSales Accounts` sa2)
		GROUP BY
			Account,tst2.sales_person
		UNION ALL
		SELECT 
			COALESCE(tst.sales_person,tst1.sales_person) as 'Sales_Person',sum(tge.debit) as 'Amount:Currency:100', 
			Min(tge.posting_date) 'Start_Date:Date:150', 
			Max(tge.posting_date) 'End_Date:Date:150',
			sa3.branch as Account
			FROM 
				`tabGL Entry` tge 
			left outer join 
				`tabJournal Entry Account` tjea 
			on 
				tge.voucher_no=tjea.parent 
			left outer join 
				`tabSales Team` tst 
			on 
				tjea.reference_name=tst.parent 
			left outer join `tabSales Team` tst1 
			on 
				tst1.parent=tge.voucher_no 
			left outer join 
				`tabJournal Entry` tje 
			on 
				tje.name=tjea.parent
			LEFT OUTER JOIN `tabSales Accounts` sa3
			ON
				sa3.account = tge.account 
			WHERE 
				(tge.posting_date between %s and %s AND tge.account in (SELECT sa5.account from `tabSales Accounts` sa5)) AND ((tge.debit >0 and tge.docstatus=1 AND tjea.reference_type in ('Sales Invoice','Sales Order')) OR tge.voucher_type='Sales Invoice') Group by Account, Sales_Person
		UNION ALL
		SELECT
			'Refund' as 'Sales_Person',-1*sum(tge.debit) as 'Amount:Currency:100', 
                        Min(tge.posting_date) 'Start_Date:Date:150', 
                        Max(tge.posting_date) 'End_Date:Date:150',
                        sa4.branch as Account
                        FROM 
                                `tabGL Entry` tge
			LEFT OUTER JOIN `tabSales Accounts` sa4
			ON sa4.account = tge.against
			WHERE 
                                (
				tge.posting_date between %s and %s 
				AND tge.account in ('Debtors - PFS','Debtors - SF','Debtors - SFPL') 
				and tge.voucher_type='Journal Entry' 
				AND tge.docstatus=1 
				)
			GROUP BY
				tge.against
                 ''', (filters.from_date, filters.to_date,filters.from_date, filters.to_date,filters.from_date, filters.to_date))

        return columns, data
