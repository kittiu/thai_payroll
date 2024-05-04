frappe.ui.form.on("Employee Tax Exemption Declaration", {

	custom_get_yearly_salary: function(frm) {
		frappe.call({
			method: "thai_payroll.custom.employee_tax_exemption_declaration.get_employee_yearly_salary",
			args: {
				company: frm.doc.company,
				payroll_period: frm.doc.payroll_period,
				employee: frm.doc.employee,
			},
			callback: function (r) {
				console.log(r.message)
				frm.set_value("custom_yearly_salary", r.message);
			},
		});
	},

})
