# -*- coding: utf-8 -*-
# Copyright (c) 2017, Togo Business Solutions and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class UserWarehousePermission(Document):
	pass

def validate_wh_allowed_for_user(doc,method):
	"""Check if the user is allowed to post to the specified warehouse"""
	user = frappe.session.user
	allowed_warehouses = frappe.get_all('User Warehouse Permission', filters={'user': user,'warehouse'=warehouse}, fields=['warehouse'])
	found = False
	#Check that each warehouse selected in items is in the user list
	for item in doc.items:
		found = False		
		for allowed_warehouse in allowed_warehouses:
			if(allowed_warehouse['warehouse'] == item.warehouse):
				found = True
		if not found:
			frappe.throw(_("User {0} is not allowed to post for warehouse {1}, item {2}.").format(user,warehouse,item.item_name))
