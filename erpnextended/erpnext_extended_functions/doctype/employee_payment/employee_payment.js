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
        },
	amount: function(frm, dt, dn) {
		cur_frm.cscript.update_totals(frm.doc);
	}
});

frappe.ui.form.on('Employee Payment', {
        journal_entry: function(frm,cdt,cdn) {
		frappe.call({
			method: "frappe.client.get_value",
			args: {
				doctype: "Journal Entry",
				filters: {"name": frm.doc.journal_entry},
				fieldname: "total_debit"
			},
			callback: function(r){
				if(r.message){
					frappe.model.set_value(cdt, cdn, "amount", r.message.total_debit);
					frappe.call({
						method: "frappe.client.get_value",
                        			args: {
                                			doctype: "Journal Entry",
                                			filters: {"name": frm.doc.journal_entry},
                                			fieldname: "posting_date"
                        			},
                        			callback: function(d){
                                			if(d.message){
                                        			frappe.model.set_value(cdt, cdn, "posting_date", d.message.posting_date);

                                			}
						}
                        		});
				}
			}
		});
	}
});

cur_frm.cscript.update_totals = function(doc) {
        var ta=0.0;
        var allocations = doc.employee_allocations || [];
        for(var i in allocations) {
                ta += flt(allocations[i].amount, precision("amount", allocations[i]));
        }
        var doc = locals[doc.doctype][doc.name];
        doc.allocated_amount = ta;
        refresh_many(['allocated_amount']);
}

cur_frm.cscript.validate = function(doc,cdt,cdn) {
        cur_frm.cscript.update_totals(doc);
}
