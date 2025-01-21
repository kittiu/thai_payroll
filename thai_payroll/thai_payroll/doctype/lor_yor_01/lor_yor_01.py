# Copyright (c) 2024, Kitti U. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from thai_payroll.mixins.thai_payroll_mixin import ThaiPayrollMixin


class LorYor01(Document, ThaiPayrollMixin):

	def validate(self):
		self.check_existing()
		self.compute_exemptions()

	def on_submit(self):
		if self.create_tax_exemption_on_submit:
			self.cancel_exiting_emp_tax_exemption()
			self.create_emp_tax_exemption()

	# On cancel of Lor Yor 01, delete any Draft Employee Tax Exemption Declaration linked to it
	def on_cancel(self):
		doc = frappe.db.get_value(
			"Employee Tax Exemption Declaration",
			{"ref_lor_yor_01": self.name, "docstatus": 0},
			"name"
		)
		if doc:
			frappe.delete_doc("Employee Tax Exemption Declaration", doc)

	def check_existing(self):
		ly01 = frappe.qb.DocType("Lor Yor 01")
		query = (
			frappe.qb.from_(ly01)
			.select(ly01.name)
			.where(
				(ly01.payroll_period == self.payroll_period)
				& (ly01.docstatus != 2)
				& (ly01.employee == self.employee)
				& (ly01.name != self.name)
			)
		)
		ret_exist = query.run()
		if ret_exist:
			frappe.throw(
				_("Lor Yor 01 of employee {0} already created for this period").format(self.employee)
			)
	
	def compute_exemptions(self):
		# Personal Exemption
		self.personal_exemption = 60000
		self.elderly_exemption = 190000 if self.elderly else 0
		self.disabled_exemption = 190000 if not self.elderly and self.disabled else 0
		# Spouse Exemption
		if self.personal_status == "สมรส" and self.spouse_financial_status == "ไม่มีเงินได้":
			self.spouse_exemption = 60000
		else:
			self.spouse_exemption = 0
		self.elderly_spouse_exemption = 190000 if self.elderly_spouse else 0
		# Child Exemption
		self.child_exemption_1_amount = int(self.child_exemption_1) * 30000
		self.child_exemption_2_amount = int(self.child_exemption_2) * 60000
		# Parent Exemption
		own_parents = sum([self.own_father_exemption, self.own_mother_exemption])
		self.total_own_parent_exemption = own_parents * 30000
		spouse_parents = sum([self.spouse_father_exemption, self.spouse_mother_exemption])
		self.total_spouse_parent_exemption = spouse_parents * 30000
		# Disable Exemption
		self.total_disabled_person_support = int(self.disabled_persons_in_support) * 60000
		if sum([
			self.insurance_own_father,
		  	self.insurance_own_mother,
		  	self.insurance_spouse_father,
		  	self.insurance_spouse_mother,
		]) == 0:
			self.total_parent_insurance = 0
		elif self.total_parent_insurance == 0:
			frappe.throw(_("Total Parent Insurance shouldn't be zero"))

		# Total Amount
		fields = frappe.get_meta(self.doctype).fields
		currency_fields = list(filter(lambda x: x.fieldtype=="Currency", fields))
		sum_fields = [x.fieldname for x in currency_fields if x.fieldname != "total_amount"]
		self.total_amount = sum(self.as_dict()[x] for x in sum_fields)

	def create_emp_tax_exemption(self):
		doc = frappe.new_doc("Employee Tax Exemption Declaration")
		doc.update({
			"company": self.company,
			"employee": self.employee,
			"payroll_period": self.payroll_period,
			"ref_lor_yor_01": self.name
		})
		# mapping from ly01 to tax exempt
		doc.custom_exemption = self.personal_exemption
		doc.custom_spouse_exemption = self.spouse_exemption
		doc.custom_elderly_exemption = self.elderly_exemption
		doc.custom_elderly_spouse_exemption = self.elderly_spouse_exemption
		doc.custom_disable_person_exemption = self.disabled_exemption
		doc.custom_child_born_before_2561 = self.child_exemption_1 if self.child_exemption_1 != "0" else ""
		doc.custom_child_born_from_2561 = self.child_exemption_2 if self.child_exemption_2 != "0" else ""
		doc.custom_total_child_exemption = self.child_exemption_1_amount + self.child_exemption_2_amount
		doc.custom_own_father_exemption = self.own_father_exemption
		doc.custom_own_mother_exemption = self.own_mother_exemption
		doc.custom_spouse_father_exemption = self.spouse_father_exemption
		doc.custom_spouse_mother_exemption = self.spouse_mother_exemption
		doc.custom_total_fathermother_exemption = self.total_own_parent_exemption + self.total_spouse_parent_exemption
		doc.custom_disable_person_support = self.total_disabled_person_support
		doc.custom_health_insurance_for_parents = self.total_parent_insurance
		doc.custom_life_insurance = self.life_insurance
		doc.custom_health_insurance = self.health_insurance
		doc.custom_pvd_contribution = self.pvd_contribution
		doc.custom_invest_in_annuity = self.annuity
		doc.custom_invest_in_rmf = self.rmf_investment
		doc.custom_invest_in_ssf = self.ssf_investment
		doc.custom_pension_life_insurance = self.pension_life_insurance
		doc.custom_interest_paid_for_housing_loan = self.interest_paid_for_housing_loan
		doc.custom_social_security = self.sso_contribution
		doc.custom_donation_for_education = self.donation_for_education
		doc.custom_other_donation = self.other_donation
		doc.custom_invest_in_thai_esg = self.thai_esg_investment
		doc.custom_economic_stimulus_allowance = self.economic_stimulus_allowance
		# --
		doc.save()

	def cancel_exiting_emp_tax_exemption(self):
		existing_doc = frappe.db.get_value(
			"Employee Tax Exemption Declaration",
			{
				"payroll_period": self.payroll_period,
				"employee": self.employee,
				"docstatus": ["<", 2]
			},
			"name"
		)
		if not existing_doc:
			return
		doc = frappe.get_doc("Employee Tax Exemption Declaration", existing_doc)
		if doc.docstatus == 0:
			doc.submit()
		doc.cancel()


@frappe.whitelist()
def enqueue_email_lor_yor_01s(names) -> None:
	"""enqueue bulk emailing Lor Yor 01"""
	import json
	if isinstance(names, str):
		names = json.loads(names)
	
	email_templates = frappe.get_list("Company", {"email_template_for_lor_yor_01": ["not in", [0, None, ""]]})
	if not email_templates:
		frappe.throw(_("No email template has been setup!"))

	frappe.enqueue(email_lor_yor_01s, names=names)
	frappe.msgprint(
		_("Lor Yor 01 emails have been enqueued for sending. Check {0} for status.").format(
			f"""<a href='{frappe.utils.get_url_to_list("Email Queue")}' target='blank'>Email Queue</a>"""
		)
	)


def email_lor_yor_01s(names) -> None:
	for name in names:
		lor_yor_01 = frappe.get_doc("Lor Yor 01", name)
		lor_yor_01.send_enqueue_email()
