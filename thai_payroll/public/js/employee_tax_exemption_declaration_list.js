frappe.listview_settings["Employee Tax Exemption Declaration"] = {
	onload: function (listview) {
		listview.page.add_menu_item(__("Email Tax Exemption Declaration to Employee"), () => {

			if (!listview.get_checked_items().length) {
				frappe.msgprint(__("Please select "));
				return;
			}

			frappe.confirm(__("Are you sure you want to email the selected Tax Exemption Declaration?"), () => {
				listview.call_for_selected_items(
					"thai_payroll.custom.employee_tax_exemption_declaration.enqueue_email_tax_exemptions",
				);
			});
		});
	},
};
