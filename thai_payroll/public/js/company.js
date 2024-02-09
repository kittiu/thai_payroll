frappe.ui.form.on("Company", {
	refresh(frm) {
		frm.set_query("custom_company_address_on_withholding_tax_cert", function (doc) {
			return {
				query: "frappe.contacts.doctype.address.address.address_query",
				filters: {
					link_doctype: "Company",
					link_name: doc.name
				}
			};
		});
	}
});
