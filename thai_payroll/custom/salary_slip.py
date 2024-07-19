import frappe
from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip

class SalarySlipThaiPayroll(SalarySlip):

	@property
	def relieving_date(self):
		if self.custom_allow_salary_slip:
			return None
		return super().relieving_date


def onload(doc, method):
	wht_cert = frappe.get_all(
		"Withholding Tax Cert Employee",
		filters={"voucher_type": "Salary Slip", "voucher_no": doc.name}
	)
	if wht_cert:
		doc.set_onload("wht_cert", wht_cert[0].name)


def update_payroll_period(doc, method):
	""" Update the payroll period in the salary slip based on the selected posting date """
	period = frappe.db.get_value(
		"Payroll Period",
		{"start_date": ["<=", doc.end_date], "end_date": [">=", doc.end_date]},
		"name"
	)
	frappe.db.set_value("Salary Slip", doc.name, "custom_payroll_period", period)
	doc.reload()


def update_last_submitted_slip(doc, method):
	""" Update the last submitted slip in the employee """
	# Update all slips for the same period to 0
	frappe.db.set_value(
		"Salary Slip",
		{
			"employee": doc.employee,
			"custom_payroll_period": doc.custom_payroll_period,
		},
		"custom_latest_slip",
		0
	)
	# Find the last submitted slip
	lastest_slip = frappe.db.get_value(
		"Salary Slip",
		{
			"employee": doc.employee,
			"custom_payroll_period": doc.custom_payroll_period,
			"docstatus": 1
		},
		"name",
		order_by="end_date DESC"
	)
	frappe.db.set_value("Salary Slip", lastest_slip, "custom_latest_slip", 1)
	doc.reload()


@frappe.whitelist()
def make_withholding_tax_cert_employee(source_name, target_doc=None):
	from frappe.model.mapper import get_mapped_doc

	def set_missing_values(source, target):
		target.run_method("validate")
		target.company_address = frappe.db.get_value(
		    "Company", source.company, "custom_company_address_on_withholding_tax_cert"
	    )
		target.income_tax_form = "PND1"
		target.voucher_type = "Salary Slip"
		target.payroll_period = source.custom_payroll_period
		target.append(
			"withholding_tax_items",
			dict(
				type_of_income="1",
				description="เงินเดือน ค่าจ้าง ฯลฯ 40(1)",
				tax_base=source.ctc,
				tax_amount=source.total_income_tax
			),
		)

	doclist = get_mapped_doc(
		"Salary Slip",
		source_name,
		{
			"Salary Slip": {
				"doctype": "Withholding Tax Cert Employee",
				"field_map": {
					"employee": "employee",
					"name": "voucher_no",
					"end_date": "date"
				},
				"validation": {"docstatus": ["=", 1]},
			},
		},
		target_doc,
		set_missing_values,
	)

	return doclist