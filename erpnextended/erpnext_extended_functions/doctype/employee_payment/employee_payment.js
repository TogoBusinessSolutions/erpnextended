// Copyright (c) 2017, Togo Business Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Payment Allocation', {
        employee: function(frm, cdt, cdn){
                var employee_payment_allocation = frappe.model.get_doc(cdt, cdn);
		if(employee_payment_allocation.employee){
                        frm.call({
                                method:
"erpnextended.erpnext_extended_functions.doctype.employee_payment.employee_payment.get_full_name",
                                args: {
                                        employee: employee_payment_allocation.employee
                                },
                                callback: function(r){
                                        frappe.model.set_value(cdt, cdn, "full_name", r.message);
                                }
                        });
                }else{
                        frappe.model.set_value(cdt, cdn, "full_name", null);
                }
        }
});

frappe.ui.form.on('Employee Payment', {
        journal_entry: function(frm, cdt, cdn){
                //var journal = frappe.model.get_doc(cdt, cdn);
                alert(frm.doc.journal_entry);
		//frappe.msgprint("{0} save the doctype ", [journal.name]);
                //frappe.model.set_value(cdt, cdn, "amount", journal.total_amount);
        }
});
