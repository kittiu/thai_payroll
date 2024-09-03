frappe.ui.form.on("Payroll Period", {

	refresh: function(frm) {

		frm.page.clear_primary_action();

		frm.add_custom_button(__("Show Active Employees"), function () {
			frm.events.get_payroll_period_employees(frm);
		}).toggleClass("btn-primary", !(frm.doc.custom_employees || []).length);

		if ((frm.doc.custom_employees || []).length) {
			frm.add_custom_button(__("Create Tax Exemption Declarations"), function () {
				frm.call("create_tax_exemption_declarations");
			}).addClass("btn-primary");
		}
		// Child Table > 50 Rows
		frm.get_field("custom_employees").grid.grid_pagination.page_length = 1000;
	},

	onload: function (frm) {
		frappe.realtime.off("completed_tax_exemption_creation");
		frappe.realtime.on("completed_tax_exemption_creation", function () {
			frm.reload_doc();
		});
	},

	get_payroll_period_employees: function (frm) {
		return frappe
			.call({
				doc: frm.doc,
				method: "fill_payroll_period_employees",
				freeze: true,
				freeze_message: __("Fetching Employees"),
			})
			.then((r) => {
				if (r.docs?.[0]?.custom_payroll_period_employees) {
					frm.dirty();
					frm.save();
				}
				frm.refresh();
				frm.scroll_to_field("custom_employees");
			});
	},

})
