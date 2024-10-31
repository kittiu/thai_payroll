frappe.ui.form.on("Employee Tax Exemption Declaration", {

	custom_get_yearly_salary: function(frm) {
		frappe.call({
			method: "thai_payroll.custom.employee_tax_exemption_declaration.get_employee_yearly_salary",
			args: {
				company: frm.doc.company,
				payroll_period: frm.doc.payroll_period,
				employee: frm.doc.employee,
				is_opening_entry: frm.doc.custom_is_opening_entry,
				opening_entry_date: frm.doc.custom_opening_entry_date
			},
			callback: function (r) {
				frm.set_value("custom_yearly_salary", r.message);
				frm.set_value("custom_yearly_bonus", 0);
			},
		});
	},

	custom_get_yearly_pvd_contribution: function(frm) {
		frappe.call({
			method: "thai_payroll.custom.employee_tax_exemption_declaration.get_employee_yearly_pvd_contribution",
			args: {
				company: frm.doc.company,
				payroll_period: frm.doc.payroll_period,
				employee: frm.doc.employee,
				is_opening_entry: frm.doc.custom_is_opening_entry,
				opening_entry_date: frm.doc.custom_opening_entry_date
			},
			callback: function (r) {
				frm.set_value("custom_pvd_contribution", r.message);
			},
		});
	},

})
