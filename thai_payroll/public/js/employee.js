frappe.ui.form.on("Employee", {
	onload: function (frm) {
		frm.set_query("custom_employee_severance_pay", function (doc) {
			return {
				filters: {
					docstatus: 1,
					employee: doc.employee
				},
			};
		});
	},
});
