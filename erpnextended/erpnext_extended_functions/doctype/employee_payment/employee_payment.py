# -*- coding: utf-8 -*-
# Copyright (c) 2017, Togo Business Solutions and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cstr, flt, fmt_money, formatdate

class EmployeePayment(Document):
	def validate(self):
		"""Set full name"""
		for allocation in self.employee_allocations:
			if not allocation.full_name:
				allocation.full_name = get_full_name(allocation.employee)
		validate_account_allowed(self.journal_entry)
		validate_amount(self.amount, self.allocated_amount)

def validate_amount(journal_amount,allocated_amount):
	if(flt(journal_amount) != flt(allocated_amount)):
		frappe.throw(_("Allocated payments total must match Journal Amount {0}.").format(journal_amount))

@frappe.whitelist()
def get_full_name(employee):
	emp = frappe.get_doc("Employee",employee)
	return emp.employee_name

@frappe.whitelist()
def get_journal_amount(journal_entry):
	jrn = frappe.get_doc("Journal Entry",journal_entry)
	return jrn.total_amount

def validate_account_allowed(journal_entry):
	"""Check if the selected account is in the allowed list"""
	allowed_accounts = frappe.get_all('Employee Payment Allowed Accounts', fields=['allowed_account'])
	journal_accounts = frappe.get_all('Journal Entry Account', filters={'parent': journal_entry}, fields=['account'])
	found = False
	for allowed_account in allowed_accounts:
		for journal_account in journal_accounts:
		 	if (allowed_account['allowed_account'] == journal_account['account']):		
				found = True
				break
	if not found:
		frappe.throw(_("Journal {0} is not a valid salary entry.").format(journal_entry))

	#If here account is valid, check if Journal exists for submitted documents
	ep = frappe.db.get_values("Employee Payment", {"journal_entry": journal_entry,"docstatus":1})
	if(ep):
		frappe.throw(_("Journal {0} alrady in allocated in {1}.").format(journal_entry,ep[0][0]))
