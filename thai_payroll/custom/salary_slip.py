import frappe
from frappe.utils import cint, flt, getdate, rounded
from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip

class SalarySlipThaiPayroll(SalarySlip):

	@property
	def relieving_date(self):
		if self.custom_allow_salary_slip:
			return None
		return super().relieving_date

	def get_amount_based_on_payment_days(self, row):
		base_30_days = frappe.db.get_value(
			"Salary Component",
			row.salary_component,
			"custom_base_on_30_days",
			cache=True
		)
		if not base_30_days:
			return super().get_amount_based_on_payment_days(row)
		
		# Thai Payroll override
		amount, additional_amount = row.amount, row.additional_amount
		timesheet_component = self._salary_structure_doc.salary_component

		if (
			self.salary_structure
			and cint(row.depends_on_payment_days)
			and cint(self.total_working_days)
			and not (
				row.additional_salary and row.default_amount
			)  # to identify overwritten additional salary
			and (
				row.salary_component != timesheet_component
				or getdate(self.start_date) < self.joining_date
				or (self.relieving_date and getdate(self.end_date) > self.relieving_date)
			)
		):
			# base_30_days
			additional_amount = flt(
				(
					flt(row.additional_amount)/30 * flt(self.payment_days)
	 				if flt(self.payment_days) < cint(self.total_working_days)
					else flt(row.additional_amount)
				),
				row.precision("additional_amount"),
			)
			amount = (
				flt(
					(
						flt(row.default_amount)/30 * flt(self.payment_days)
						if flt(self.payment_days) < cint(self.total_working_days)
						else flt(row.default_amount)
					),
					row.precision("amount"),
				)
				+ additional_amount
			)

		elif (
			not self.payment_days
			and row.salary_component != timesheet_component
			and cint(row.depends_on_payment_days)
		):
			amount, additional_amount = 0, 0
		elif not row.amount:
			amount = flt(row.default_amount) + flt(row.additional_amount)

		# apply rounding
		if frappe.db.get_value(
			"Salary Component", row.salary_component, "round_to_the_nearest_integer", cache=True
		):
			amount, additional_amount = rounded(amount or 0), rounded(additional_amount or 0)

		return amount, additional_amount


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
		target.income_tax_form = "PND1a"
		target.voucher_type = "Salary Slip"
		target.payroll_period = source.custom_payroll_period
		target.append(
			"withholding_tax_items",
			dict(
				type_of_income="1",
				description="เงินเดือน ค่าจ้าง ฯลฯ 40(1)",
				tax_base=source.ctc,
				tax_amount=source.income_tax_deducted_till_date
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