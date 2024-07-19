frappe.ui.form.on("Salary Slip", {

	refresh: function(frm) {
		frm.events.create_custom_buttons(frm);
	},

	create_custom_buttons: function(frm) {
		if (frm.doc.docstatus == 1) {
			if (frm.doc.__onload && frm.doc.__onload.wht_cert) {
				$('[data-doctype="Withholding Tax Cert Employee"]').find("button").hide();
				frm.add_custom_button(__("Withholding Tax Cert Employee"), function() {
					frappe.set_route("Form", "Withholding Tax Cert Employee", frm.doc.__onload.wht_cert);
				}).addClass("btn-primary");
			} else if (frm.doc.custom_latest_slip == 1) {
				$('[data-doctype="Withholding Tax Cert Employee"]').find("button").show();
				frm.add_custom_button(__("Withholding Tax Cert Employee"), function() {
					frappe.model.open_mapped_doc({
						method: "thai_payroll.custom.salary_slip.make_withholding_tax_cert_employee",
						frm: frm
					}) }, __('Create')
				);
			}
		}
	},

})
