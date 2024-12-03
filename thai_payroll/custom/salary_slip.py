import frappe
from frappe.utils import cint, flt, getdate, rounded
from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip
from thai_payroll.custom.employee_tax_exemption_declaration import (
    get_employee_yearly_pvd_contribution,
    get_employee_yearly_salary
)
from hrms.payroll.doctype.payroll_period.payroll_period import get_payroll_period


class SalarySlipThaiPayroll(SalarySlip):

	def validate(self):
		auto_revise_tax_exemption_declaration(self)
		skip_validate = frappe.get_cached_value(
			"Company", self.company, "no_salary_recompute_on_submit"
		)
		if self._action == "submit" and skip_validate:
			return
		super().validate()

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

	def get_opening_for(self, field_to_select, start_date, end_date):
		# Only if salary slip is same period as the first salary slip to use opening amount
		# Issue https://github.com/frappe/hrms/issues/2468 and PR https://github.com/frappe/hrms/pull/2469
		first_ss = frappe.db.get_value(
			"Salary Slip",
			{
				"employee": self.employee,
				"docstatus": 1,
				"company": self.company,
			},
			"name",
			order_by="start_date asc",
		)
		if first_ss:
			doc = frappe.get_cached_doc("Salary Slip", first_ss)
			if self.payroll_period != doc.payroll_period:
				return 0
		# Otherwise, find amount from first SSA which has opening balance
		ssa_opening = frappe.db.get_value(
			"Salary Structure Assignment",
			{
				"employee": self.employee,
				"docstatus": 1,
				"company": self.company,
				field_to_select: [">", 0],
			},
			field_to_select,
			order_by="from_date asc",
		)
		return ssa_opening or 0


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


def auto_revise_tax_exemption_declaration(doc):
	use_thai_pit, auto_revise = frappe.get_cached_value(
		"Company", doc.company,
		["custom_use_thai_pit_calculation", "custom_auto_revise_tax_exemption_declaration"]
	)
	if not (use_thai_pit and auto_revise):
		return

	# Get existing salary and pvd
	tax_exempt = frappe.db.get_value(
		"Employee Tax Exemption Declaration",
		{"employee": doc.employee, "payroll_period": doc.payroll_period.name, "docstatus": 1},
		["name", "custom_is_opening_entry", "custom_opening_entry_date", "custom_yearly_salary", "custom_pvd_contribution"],
		as_dict=1,
		cache=True,
	)
	if not tax_exempt:
		return
	# Get new salary and pvd
	params = {
		"company": doc.company,
		"payroll_period": doc.payroll_period,
		"employee": doc.employee,
		"is_opening_entry": tax_exempt.custom_is_opening_entry,
		"opening_entry_date": tax_exempt.custom_opening_entry_date
	}
	new_salary = get_employee_yearly_salary(**params)
	new_pvd = get_employee_yearly_pvd_contribution(**params)
	# If diff, do the revision
	if (
		flt(new_salary, 2) != flt(tax_exempt.custom_yearly_salary, 2)
		or flt(new_pvd, 2) != flt(tax_exempt.custom_pvd_contribution, 2)
	):
		old_doc = frappe.get_cached_doc("Employee Tax Exemption Declaration", tax_exempt.name)
		old_doc.cancel()
		new_doc = frappe.copy_doc(old_doc)
		new_doc.docstatus = 0
		new_doc.custom_yearly_salary = new_salary
		new_doc.custom_pvd_contribution = new_pvd
		new_doc.amended_from = old_doc.name
		new_doc.save()
		new_doc.submit()
