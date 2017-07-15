frappe.ui.form.on('Employee Payment Allocation', {
        employee_payment_allocation: function{frm, cdt, cdn){
                var employee_payment_allocation = frappe.model.get_doc(cdt, cdn);
                if(employee_payment_allocation.employee){
                        frm.call({
                                method: "erpnext_extended_functions.employee_payment.doctype$
                                args: {
                                        employee: employee_allocations.employee
                                },
                                callback: function(r){
                                        frappe.model.set_value(cdt, cdn, "full_name", r.mess$
                                }
                        });
                }else{
                        frappe.model.set_value(cdt, cdn, "full_name", null);
                }
        }
});
