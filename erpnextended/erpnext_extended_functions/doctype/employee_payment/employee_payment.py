# -*- coding: utf-8 -*-
# Copyright (c) 2017, Togo Business Solutions and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class EmployeePayment(Document):
<<<<<<< HEAD
	def validate(self):
		"""Set full name"""
		for allocation in self.employee_allocations:
			if not allocation.full_name:
				allocation.full_name = get_full_name(allocation.employee)

@frappe.whitelist()
def get_full_name(employee):
	emp = frappe.get_doc("Employee",employee)
	return emp.employee_name
=======
        def validate(self):
                """Set full name"""
                for allocation in self.employee_allocations:
                        if not allocation.full_name:
                                allocation.full_name = get_full_name(allocation.employee)

@frappe.whitelist()
def get_full_name(employee):
        emp = frappe.get_doc("Employee",employee)
        return emp.employee_name

>>>>>>> 446b7d4285e003fda741fefb5c7fd9502f1b0394
