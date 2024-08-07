// Copyright (c) 2024, Kitti U. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee Severance Pay", {

	setup: function (frm) {
		frm.set_query("income_tax_slab", function () {
			return {
				filters: {
					company: frm.doc.company,
					docstatus: 1,
					disabled: 0,
					currency: frm.doc.currency,
				},
			};
		});
    },

	onload: function (frm) {
		if (!frm.doc.income_tax_slab) {
			frappe.db.get_single_value("Severance Pay Settings", "income_tax_slab").then((value) => {
				if (value) { frm.set_value("income_tax_slab", value); }
			})
		}
	}

});
