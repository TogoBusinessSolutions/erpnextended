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
                {
                        'fieldname': 'Territory',
                        'fieldtype': 'data',
                        'label': 'Territory'
                },
                {
                        'fieldname': 'Transaction',
                        'fieldtype': 'data',
                        'label': 'Transaction'
                }
        ]

        data = frappe.db.sql('''SELECT
		tst2.sales_person as 'Sales_Person', 
		SUM(tpe.paid_amount) as 'Amount',
		MIN(tpe.posting_date) as 'Start_date',
		MAX(tpe.posting_date) as 'End_Date',
		CASE tpe.paid_to 
			WHEN 'Cash - PFS' THEN 'Randburg' 
			WHEN 'Cash Cosmo - PFS' THEN 'Cosmo' 
			WHEN 'Standard Bank Cosmo - PFS' THEN 'Cosmo' 
			WHEN 'Standard Bank - PFS' THEN 'Randburg' 
			WHEN 'Standard Bank Warehouse - PFS' THEN 'Warehouse'
			WHEN 'Standard Bank Mall - PFS' THEN 'Mall'
			WHEN 'Cash - Mall - PFS' THEN 'Mall'
			WHEN 'Cash - Warehouse - PFS' THEN 'Warehouse'
			WHEN 'Standard Bank - hahashu - PFS' THEN 'hahashu.co.za'
			When 'Cash hahashu.co.za - PFS' THEN 'hahashu.co.za'
			WHEN 'Standard Bank Fourways - PFS' THEN 'Fourways'
			When 'Cash Fourways - PFS' THEN 'Fourways'
			When 'Cash Boulders - PFS' THEN 'Boulders'
			When 'Standard Bank Boulders - PFS' THEN 'Boulders'
		END as Account,
		tsi.territory as Territory,
		'Sales Invoice' as Transaction
		FROM 
			`tabPayment Entry` tpe
		INNER JOIN
			`tabPayment Entry Reference` ter
		ON
			tpe.name=ter.parent
		LEFT OUTER JOIN
			`tabSales Team` tst2 
		ON
			tst2.parent=ter.reference_name
		INNER JOIN
			`tabSales Invoice` tsi
		ON
			ter.reference_name = tsi.name 
		WHERE
			tpe.posting_date between %s and %s
		AND 
			tpe.docstatus=1
		AND
			tpe.payment_type='Receive'
		AND tpe.paid_to in ('Cash - PFS','Cash Cosmo - PFS','Standard Bank Cosmo - PFS','Standard Bank - PFS','Standard Bank Mall - PFS','Standard Bank Warehouse - PFS','Cash - Mall - PFS','Cash - Warehouse - PFS','Standard Bank - hahashu - PFS','Cash hahashu.co.za - PFS','Standard Bank Fourways - PFS','Cash Fourways - PFS','Cash Boulders - PFS','Standard Bank Boulders - PFS')
		GROUP BY
			Account,tst2.sales_person,Territory,Transaction
		UNION ALL
		SELECT
		tst2_so.sales_person as 'Sales_Person', 
		SUM(tpe_so.paid_amount) as 'Amount',
		MIN(tpe_so.posting_date) as 'Start_date',
		MAX(tpe_so.posting_date) as 'End_Date',
		CASE tpe_so.paid_to 
			WHEN 'Cash - PFS' THEN 'Randburg' 
			WHEN 'Cash Cosmo - PFS' THEN 'Cosmo' 
			WHEN 'Standard Bank Cosmo - PFS' THEN 'Cosmo' 
			WHEN 'Standard Bank - PFS' THEN 'Randburg' 
			WHEN 'Standard Bank Warehouse - PFS' THEN 'Warehouse'
			WHEN 'Standard Bank Mall - PFS' THEN 'Mall'
			WHEN 'Cash - Mall - PFS' THEN 'Mall'
			WHEN 'Cash - Warehouse - PFS' THEN 'Warehouse'
			WHEN 'Standard Bank - hahashu - PFS' THEN 'hahashu.co.za'
			When 'Cash hahashu.co.za - PFS' THEN 'hahashu.co.za'
			WHEN 'Standard Bank Fourways - PFS' THEN 'Fourways'
			When 'Cash Fourways - PFS' THEN 'Fourways'
			When 'Cash Boulders - PFS' THEN 'Boulders'
			When 'Standard Bank Boulders - PFS' THEN 'Boulders'
		END as Account,
		tso_so.territory as Territory,
		'Sales Order' as Transaction
		FROM 
			`tabPayment Entry` tpe_so
		INNER JOIN
			`tabPayment Entry Reference` ter_so
		ON
			tpe_so.name=ter_so.parent
		LEFT OUTER JOIN
			`tabSales Team` tst2_so 
		ON
			tst2_so.parent=ter_so.reference_name
		INNER JOIN
			`tabSales Order` tso_so
		ON
			ter_so.reference_name = tso_so.name 
		WHERE
			tpe_so.posting_date between %s and %s
		AND 
			tpe_so.docstatus=1
		AND
			tpe_so.payment_type='Receive'
		AND tpe_so.paid_to in ('Cash - PFS','Cash Cosmo - PFS','Standard Bank Cosmo - PFS','Standard Bank - PFS','Standard Bank Mall - PFS','Standard Bank Warehouse - PFS','Cash - Mall - PFS','Cash - Warehouse - PFS','Standard Bank - hahashu - PFS','Cash hahashu.co.za - PFS','Standard Bank Fourways - PFS','Cash Fourways - PFS','Cash Boulders - PFS','Standard Bank Boulders - PFS')
		GROUP BY
			Account,tst2_so.sales_person,Territory,Transaction
		UNION ALL
		SELECT 
			COALESCE(tst.sales_person,tst1.sales_person) as 'Sales_Person',sum(tge.debit) as 'Amount:Currency:100', 
			Min(tge.posting_date) 'Start_Date:Date:150', 
			Max(tge.posting_date) 'End_Date:Date:150',
			CASE tge.account 
				WHEN 'Cash - PFS' THEN 'Randburg' 
				WHEN 'Cash Cosmo - PFS' THEN 'Cosmo' 
				WHEN 'Standard Bank Cosmo - PFS' THEN 'Cosmo' 
				WHEN 'Standard Bank - PFS' THEN 'Randburg'
				WHEN 'Standard Bank Warehouse - PFS' THEN 'Warehouse'
				WHEN 'Standard Bank Mall - PFS' THEN 'Mall'
				WHEN 'Cash - Mall - PFS' THEN 'Mall'
				WHEN 'Cash - Warehouse - PFS' THEN 'Warehouse' 
				WHEN 'Standard Bank - hahashu - PFS' THEN 'hahashu.co.za'
				When 'Cash hahashu.co.za - PFS' THEN 'hahashu.co.za'
				WHEN 'Standard Bank Fourways - PFS' THEN 'Fourways'
				When 'Cash Fourways - PFS' THEN 'Fourways'
				When 'Cash Boulders - PFS' THEN 'Boulders'
                        	When 'Standard Bank Boulders - PFS' THEN 'Boulders'
			END 
				as Account,
			tsi1.territory as Territory,
			'Sales Invoice' as Transaction
			FROM 
				`tabGL Entry` tge 
			left outer join 
				`tabJournal Entry Account` tjea 
			on 
				tge.voucher_no=tjea.parent
			inner join `tabSales Invoice` tsi1
			on 
				tsi1.name = tge.voucher_no
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
			WHERE 
				(tge.posting_date between %s and %s AND tge.account in ('Cash - PFS','Cash Cosmo - PFS','Standard Bank Cosmo - PFS','Standard Bank - PFS','Standard Bank Mall - PFS','Standard Bank Warehouse - PFS','Cash - Mall - PFS','Cash - Warehouse - PFS','Standard Bank - hahashu - PFS','Cash hahashu.co.za - PFS','Standard Bank Fourways - PFS','Cash Fourways - PFS','Cash Boulders - PFS','Standard Bank Boulders - PFS')) AND ((tge.debit >0 and tge.docstatus=1 AND tjea.reference_type in ('Sales Invoice','Sales Order')) OR tge.voucher_type='Sales Invoice') 
				Group by Account, Sales_Person,Territory,Transaction
		UNION ALL
		SELECT
			'Refund' as 'Sales_Person',-1*sum(tge.debit) as 'Amount:Currency:100', 
                        Min(tge.posting_date) 'Start_Date:Date:150', 
                        Max(tge.posting_date) 'End_Date:Date:150',
                        CASE tge.against
                                WHEN 'Cash - PFS' THEN 'Randburg' 
                                WHEN 'Cash Cosmo - PFS' THEN 'Cosmo' 
                                WHEN 'Standard Bank Cosmo - PFS' THEN 'Cosmo' 
                                WHEN 'Standard Bank - PFS' THEN 'Randburg'
                                WHEN 'Standard Bank Warehouse - PFS' THEN 'Warehouse'
                                WHEN 'Standard Bank Mall - PFS' THEN 'Mall'
                                WHEN 'Cash - Mall - PFS' THEN 'Mall'
                                WHEN 'Cash - Warehouse - PFS' THEN 'Warehouse' 
                                WHEN 'Standard Bank - hahashu - PFS' THEN 'hahashu.co.za'
                                When 'Cash hahashu.co.za - PFS' THEN 'hahashu.co.za'
                                WHEN 'Standard Bank Fourways - PFS' THEN 'Fourways'
                                When 'Cash Fourways - PFS' THEN 'Fourways'
                                When 'Cash Boulders - PFS' THEN 'Boulders'
                                When 'Standard Bank Boulders - PFS' THEN 'Boulders'
                        END 
                                as Account,
						'' as Territory,
						'Refund' as Transaction
                        FROM 
                                `tabGL Entry` tge
			WHERE 
                                (
				tge.posting_date between %s and %s 
				AND account = 'Debtors - PFS' 
				and voucher_type='Journal Entry' 
				AND docstatus=1 
				)
			GROUP BY
				tge.against,Territory,Transaction
                 ''', (filters.from_date, filters.to_date,filters.from_date, filters.to_date,filters.from_date, filters.to_date,filters.from_date, filters.to_date))

        return columns, data
