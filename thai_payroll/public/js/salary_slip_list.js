frappe.listview_settings["Salary Slip"] = {

	onload: function(listview) {

		// Override apps/hrms/hrms/payroll/doctype/salary_slip/salary_slip_list.js
		if (!has_common(frappe.user_roles, ["Administrator", "System Manager", "HR Manager", "HR User"])) return;

		listview.page.add_menu_item(__("Email Salary Slips"), () => {
			if (!listview.get_checked_items().length) {
				frappe.msgprint(__("Please select the salary slips to email"));
				return;
			}

			frappe.confirm(__("Are you sure you want to email the selected salary slips?"), () => {
				listview.call_for_selected_items("hrms.payroll.doctype.salary_slip.salary_slip.enqueue_email_salary_slips");
			});
		});
		// --
	
		// Addition
		listview.page.add_action_item(__("Withholding Tax Cert Employee"), ()=>{
			erpnext.bulk_transaction_processing.create(
				listview,
				"Salary Slip",
				"Withholding Tax Cert Employee"
			);
		});
	}

};
