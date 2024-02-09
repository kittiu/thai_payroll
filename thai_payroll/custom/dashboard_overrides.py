from frappe import _


def get_dashboard_data_for_salary_slip(data):
	data["non_standard_fieldnames"].update({"Withholding Tax Cert Employee": "voucher_no"})
	data["transactions"].append({"items": ["Withholding Tax Cert Employee"]})
	return data
