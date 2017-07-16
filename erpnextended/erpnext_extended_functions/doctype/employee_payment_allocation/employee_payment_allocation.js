frappe.ui.form.on('Employee Payment Allocation', {
	employee_payment_allocation: function{frm, cdt, cdn){
		var employee_payment_allocation = frappe.model.get_doc(cdt, cdn);
		if(employee_payment_allocation.employee){
			frm.call({
<<<<<<< HEAD
				method: 
"erpnext_extended_functions.employee_payment.doctype.erpnext_extended_functions.employee_payment.get_full_name",
=======
				method: "erpnext_extended_functions.employee_payment.doctype.erpnext_extended_functions.employee_payment.get_full_name",
>>>>>>> 446b7d4285e003fda741fefb5c7fd9502f1b0394
				args: {
					employee: employee_allocations.employee
				},
				callback: function(r){
<<<<<<< HEAD
					frappe.model.set_value(cdt, cdn, "full_name", r.message);
=======
					frappe.model.set_value(cdt, cdn, "full_name", r.message); 
>>>>>>> 446b7d4285e003fda741fefb5c7fd9502f1b0394
				}
			});
		}else{
			frappe.model.set_value(cdt, cdn, "full_name", null);
		}
	}
});
