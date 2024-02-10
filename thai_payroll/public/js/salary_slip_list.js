frappe.listview_settings["Salary Slip"] = {

	onload: function(listview) {
		listview.page.add_action_item(__("Withholding Tax Cert Employee"), ()=>{
			erpnext.bulk_transaction_processing.create(
				listview,
				"Salary Slip",
				"Withholding Tax Cert Employee"
			);
		});
	}

};
