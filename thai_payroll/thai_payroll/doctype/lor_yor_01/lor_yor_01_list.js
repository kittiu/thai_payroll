frappe.listview_settings["Lor Yor 01"] = {
	onload: function (listview) {
		listview.page.add_menu_item(__("Email Lor Yor 01 to Employee"), () => {

			if (!listview.get_checked_items().length) {
				frappe.msgprint(__("Please select "));
				return;
			}

			frappe.confirm(__("Are you sure you want to email the selected Lor.Yor.01?"), () => {
				listview.call_for_selected_items(
					"thai_payroll.thai_payroll.doctype.lor_yor_01.lor_yor_01.enqueue_email_lor_yor_01s",
				);
			});
		});
	},
};
