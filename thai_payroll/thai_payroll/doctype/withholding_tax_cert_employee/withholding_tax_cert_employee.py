# Copyright (c) 2024, Kitti U. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class WithholdingTaxCertEmployee(Document):

	def validate(self):
		if not self.voucher_no:
			return
		wht_cert = frappe.db.exists(
			"Withholding Tax Cert Employee", {
				"voucher_type": "Salary Slip",
				"voucher_no": self.voucher_no,
				"docstatus": ["!=", 2]
			}
		)
		if wht_cert and wht_cert != self.name:
			frappe.throw(
				_("Withholding Tax Cert: {0} is already for Salary Slip: {1}").format(
					frappe.bold(wht_cert), frappe.bold(self.voucher_no)
				)
			)

	def before_insert(self):
		self.submitted_by = None

	def before_submit(self):
		self.submitted_by = frappe.session.user