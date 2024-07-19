from frappe import _


def get_dashboard_data_for_payroll_period(data):
	data["non_standard_fieldnames"].update({
		"Salary Slip": "custom_payroll_period",
		"Withholding Tax Cert Employee": "payroll_period",
	})
	data["transactions"].append({
		"items": ["Salary Slip", "Withholding Tax Cert Employee"]
	})
	return data
