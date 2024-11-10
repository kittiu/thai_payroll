import frappe
from frappe import _, msgprint
from frappe.utils.background_jobs import enqueue


class ThaiPayrollMixin:
	"""Mixin class for common features in payroll doctypes"""

	def send_enqueue_email(self):
		""" Send email using email template """
		company = frappe.get_cached_doc("Company", self.company)
		receiver_email = frappe.db.get_value("Employee", self.employee, "prefered_email", cache=True)
		sender_email = frappe.db.get_value("Email Account", {"default_outgoing": 1}, "email_id", cache=True)  # Default
		if company.thai_payroll_email_sender:  # If specified
			sender_email = frappe.db.get_value("Contact", company.thai_payroll_email_sender, "email_id", cache=True)

		email_template = None
		if self.doctype == "Lor Yor 01":
			email_template = company.email_template_for_lor_yor_01
		if self.doctype == "Employee Tax Exemption Declaration":
			email_template = company.email_template_for_tax_exempt_declaration

		if email_template:
			email_template = frappe.get_doc("Email Template", email_template)
			context = self.as_dict()
			subject = frappe.render_template(email_template.subject, context)
			message = frappe.render_template(email_template.response, context)
		else:
			msgprint(_("{0}: Email template is not set, hence email not sent").format(self.employee_name))
			return

		if receiver_email:
			email_args = {
				"sender": sender_email,
				"recipients": [receiver_email],
				"message": message,
				"subject": subject,
				"reference_doctype": self.doctype,
				"reference_name": self.name,
			}
			if not frappe.flags.in_test:
				enqueue(method=frappe.sendmail, queue="short", timeout=300, is_async=True, **email_args)
			else:
				frappe.sendmail(**email_args)
		else:
			msgprint(_("{0}: Employee email not found, hence email not sent").format(self.employee_name))
