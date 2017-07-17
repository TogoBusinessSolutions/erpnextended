# -*- coding: utf-8 -*-
# Copyright (c) 2017, Togo Business Solutions and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class EmployeePayment(Document):
	def validate(self):
		"""Set full name"""
		for allocation in self.employee_allocations:
			if not allocation.full_name:
				allocation.full_name = get_full_name(allocation.employee)
		validate_account_allowed(self.journal_entry)

@frappe.whitelist()
def get_full_name(employee):
	emp = frappe.get_doc("Employee",employee)
	return emp.employee_name

def validate_account_allowed(journal_entry):
	"""Check if the selected account is in the allowed list"""
	allowed_accounts = frappe.get_all('Employee Payment Allowed Accounts', fields=['allowed_account'])
	journal_accounts = frappe.get_all('Journal Entry Account', filters={'parent': journal_entry}, fields=['account'])
	found = False
	for allowed_account in allowed_accounts:
		for journal_account in journal_accounts:
		 	if (allowed_accounts[allowed_account] == journal_accounts[journal_account]):		
				found = True
				break
	if not found:
		frappe.throw(_("Journal {0},{1} not valid for salary/wage accounts.").format(allowed_accounts,journal_accounts))
