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
				}, __("View"));
			} else {
				$('[data-doctype="Withholding Tax Cert Employee"]').find("button").show();
				frm.add_custom_button(__("Withholding Tax Cert Employee"), function() {
					frappe.call({
						method: "thai_payroll.custom.custom_api.make_withholding_tax_cert_employee",
						args: {
							doc: frm.doc,
						},
						callback: function (r) {
							var doclist = frappe.model.sync(r.message);
							frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
						},
					});
				}, __("Create"));
			}
		}
	},

})
