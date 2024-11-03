# Copyright (c) 2024, Kitti U. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class LorYor01(Document):

	def validate(self):
		self.check_existing()
		self.compute_exemptions()

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
		# Spouse Exemption
		if self.personal_status == "สมรส" and self.spouse_financial_status == "ไม่มีเงินได้":
			self.spouse_exemption = 60000
		else:
			self.spouse_exemption = 0
		# Child Exemption
		self.child_exemption_1_amount = int(self.child_exemption_1) * 30000
		self.child_exemption_2_amount = int(self.child_exemption_2) * 60000
		# Parent Exemption
		own_parents = sum([self.own_father_exemption, self.own_mother_exemption])
		self.total_own_parent_exemption = own_parents * 30000
		spouse_parents = sum([self.spouse_father_exemption, self.spouse_mother_exemption])
		self.total_spouse_parent_exemption = spouse_parents * 30000
		# Disable Exemption
		self.total_disable_person_support = int(self.disable_persons_in_support) * 60000
		if sum([
			self.insurance_own_father,
		  	self.insurance_own_mother,
		  	self.insurance_spouse_father,
		  	self.insurance_spouse_mother,
		]) == 0:
			self.total_parent_insurance = 0
