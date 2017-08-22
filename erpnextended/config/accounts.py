
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Employee Payments"),
			"items": [
				{
					"type": "doctype",
					"name": "Employee Payment",
					"label": _("Employee Payment"),
					"description": _("Allocate Employee payments"),
				},
				{
					"type": "report",
					"name": "Employee Payments",
					"doctype": "Employee Payment",
					"is_query_report": True,
					"description": _("Employee Payments Summary")
				},
				{
                                        "type": "report",
                                        "name": "Unallocated Salary Journals",
                                        "doctype": "Journal Entry",
                                        "is_query_report": True,
					"description": _("Unallocated Salary Journals")
                                }
			]
		},
		{
			"label": _("Sales Reports"),
                        "items": [
                                {
                                        "type": "report",
                                        "name": "Commissions Summary By Sales Person",
                                        "doctype": "Journal Entry",
                                        "is_query_report": True,
                                        "description": _("Commissions Summary By Sales Person")
                                }
                        ]
		}
	]
