function extend_listview_event(doctype, event, callback) {
    if (!frappe.listview_settings[doctype]) {
        frappe.listview_settings[doctype] = {};
    }

    const old_event = frappe.listview_settings[doctype][event];
    frappe.listview_settings[doctype][event] = function (listview) {
        if (old_event) {
            old_event(listview);
        }
        callback(listview);
    }
}

extend_listview_event("Salary Slip", "onload", function (listview) {
	listview.page.add_action_item(__("Withholding Tax Cert Employee"), ()=>{
		erpnext.bulk_transaction_processing.create(
			listview,
			"Salary Slip",
			"Withholding Tax Cert Employee"
		);
	});
});
