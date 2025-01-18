import json
import frappe
from frappe import _
from hrms.payroll.doctype.payroll_period.payroll_period import PayrollPeriod
from frappe.utils import get_link_to_form
from frappe.query_builder import Order


class PayrollPeriodThaiPayroll(PayrollPeriod):

	@frappe.whitelist()
	def fill_payroll_period_employees(self):
		filters = frappe._dict(
			payroll_period=self.name,
			company=self.company,
			branch=self.custom_branch,
			department=self.custom_department,
			designation=self.custom_designation,
			grade=self.custom_grade,
			start_date=self.start_date,
			end_date=self.end_date,
		)
		employees = get_employee_list(filters)
		self.set("custom_employees", [])
		if not employees:
			error_msg = _("No employees found for the mentioned criteria:")
			if self.custom_branch:
				error_msg += "<br>" + _("Branch: {0}").format(frappe.bold(self.custom_branch))
			if self.custom_department:
				error_msg += "<br>" + _("Department: {0}").format(frappe.bold(self.custom_department))
			if self.custom_designation:
				error_msg += "<br>" + _("Designation: {0}").format(frappe.bold(self.custom_designation))
			if self.custom_grade:
				error_msg += "<br>" + _("Grade: {0}").format(frappe.bold(self.custom_grade))
			frappe.throw(error_msg, title=_("No employees found"))
		self.set("custom_employees", employees)
		self.custom_number_of_employees = len(self.custom_employees)


	@frappe.whitelist()
	def create_tax_exemption_document(self, doctype):
		"""
		Creates tax exemption for employee if not already created.
		"""
		check_has_doc = {
			"Employee Tax Exemption Declaration": "has_tax_exemption_declaration",
			"Lor Yor 01": "has_lor_yor_01",
		}
		self.check_permission("write")
		emp_without_ssa = [
			"{}: {}".format(emp.employee, emp.employee_name)
			for emp in self.custom_employees if not emp.has_salary_structure_assignment
		]
		emp_to_create = [
			emp.employee for emp in self.custom_employees
			if (
				emp.has_salary_structure_assignment
				and not emp.as_dict().get(check_has_doc[doctype])
			)
		]
		if emp_to_create:
			args = frappe._dict(
				{
					"company": self.company,
					"payroll_period": self.name,
				}
			)
			if len(emp_to_create) > 30 or frappe.flags.enqueue_payroll_period:
				self.db_set("custom_status", "Queued")
				frappe.enqueue(
					create_tax_exemption_for_employees,
					timeout=3000,
					doctype=doctype,
					employees=self.custom_employees,
					emp_to_create=emp_to_create,
					args=args,
					publish_progress=True,
				)
			else:
				count = create_tax_exemption_for_employees(
					doctype=doctype,
					employees=self.custom_employees,
					emp_to_create=emp_to_create,
					args=args,
					publish_progress=False
				)
				frappe.msgprint(_("Successfully created {} for {} employees").format(doctype, count))
		else:
			frappe.msgprint(_("No Tax Exemption Document created"))
			self.custom_number_of_employees = 0
			self.custom_employees = []
			self.save()
			frappe.publish_realtime("completed_tax_exemption_creation", user=frappe.session.user)
		if emp_without_ssa:
			frappe.msgprint(_("Employee without Salary Structure Assignment:<br> {0}").format("<br>".join(emp_without_ssa)))


def get_employee_list(filters):
	emp_list = get_filtered_employees(filters)
	check_emp_recent_tax_exemption(filters, emp_list)
	check_emp_salary_assignment_exists(filters.payroll_period, emp_list)
	check_emp_tax_exemption_exists(filters.payroll_period, emp_list)
	return emp_list


def get_filtered_employees(filters):
	Employee = frappe.qb.DocType("Employee")
	query = (
		frappe.qb.from_(Employee)
		.select(
			Employee.employee,
			Employee.employee_name,
			Employee.department,
			Employee.designation
		).distinct()
		.where(
			(Employee.status != "Inactive")
			& (Employee.company == filters.company)
			& ((Employee.date_of_joining <= filters.end_date) | (Employee.date_of_joining.isnull()))
			& ((Employee.relieving_date >= filters.start_date) | (Employee.relieving_date.isnull()))
		)
	)
	query = set_filter_conditions(query, filters, qb_object=Employee)
	return query.run(as_dict=True)


def get_previous_period(filters):
	prev_period = frappe.db.get_value(
		"Payroll Period",
		{
			"company": filters.company,
			"end_date": ("<", filters.start_date),
		},
		"name",
		order_by="end_date desc",
	)
	return prev_period


def get_emp_with_recent_doc(employees, doctype, prev_period):
	print(doctype)
	emp_with_doc = frappe.get_list(
		doctype,
		filters={
			"employee": ("in", employees),
			"payroll_period": prev_period,
			"docstatus": 1,
		},
		fields=["employee", "name"],
	)
	return {emp["employee"]: emp["name"] for emp in emp_with_doc}


def check_emp_recent_tax_exemption(filters, emp_list):
	check_doctypes = {
		"Employee Tax Exemption Declaration": "recent_tax_exemption",
		"Lor Yor 01": "recent_lor_yor_01"
	}
	prev_period = get_previous_period(filters)
	if not prev_period:
		return
	employees = [emp.employee for emp in emp_list]
	# Find all previous period tax exempt doctypes
	for doctype, docfield in check_doctypes.items():
		emp_with_doc = get_emp_with_recent_doc(employees, doctype, prev_period)
		for emp in emp_list:
			emp[docfield] = emp_with_doc.get(emp.employee)


def check_emp_salary_assignment_exists(payroll_period, emp_list):
	period_doc = frappe.get_cached_doc("Payroll Period", payroll_period)
	employees = [emp.employee for emp in emp_list]
	emp_with_ssa = []
	for employee in employees:
		ssa = frappe.qb.DocType("Salary Structure Assignment")
		query = (
			frappe.qb.from_(ssa)
			.select(ssa.salary_structure)
			.where(
				(ssa.docstatus == 1)
				& (ssa.employee == employee)
				& (ssa.from_date <= period_doc.end_date)
			)
			.orderby(ssa.from_date, order=Order.desc)
			.limit(1)
		)
		st_name = query.run()
		if st_name:
			emp_with_ssa.append(employee)
	emp_list = [emp for emp in emp_list if emp.employee in emp_with_ssa]
	for emp in emp_list:
		emp["has_salary_structure_assignment"] = 1
	return emp_with_ssa


def check_emp_tax_exemption_exists(payroll_period, emp_list):
	check_doctypes = {
		"Employee Tax Exemption Declaration": "has_tax_exemption_declaration",
		"Lor Yor 01": "has_lor_yor_01"
	}
	employees = [emp.employee for emp in emp_list]
	for doctype, docfield in check_doctypes.items():

		emp_with_doc = frappe.get_list(
			doctype,
			filters={
				"employee": ("in", employees),
				"docstatus": ["!=", 2],
				"payroll_period": payroll_period,
			},
			pluck="employee",
		)
		for emp in emp_list:
			if emp["employee"] in emp_with_doc:
				emp[docfield] = 1


def set_filter_conditions(query, filters, qb_object):
	"""Append optional filters to employee query"""
	if filters.get("employees"):
		query = query.where(qb_object.name.notin(filters.get("employees")))
	for fltr_key in ["branch", "department", "designation", "grade"]:
		if filters.get(fltr_key):
			query = query.where(qb_object[fltr_key] == filters[fltr_key])
	return query


def create_tax_exemption_for_employees(
        doctype,
        employees,
        emp_to_create,
        args,
        publish_progress=True
    ):
	check_recent_doc = {
		"Employee Tax Exemption Declaration": "recent_tax_exemption",
		"Lor Yor 01": "recent_lor_yor_01",
	}
	field = check_recent_doc[doctype]
	payroll_period = frappe.get_cached_doc("Payroll Period", args.payroll_period)
	try:
		employees = {emp.employee: emp.get(field) for emp in employees}
		count = 0
		for emp in emp_to_create:
			doc = args.copy()
			if employees.get(emp):  # Use recent tax exemption document if exists
				recent_doc = frappe.get_cached_doc(doctype, employees[emp]).as_dict()
				recent_doc.update(doc)
				doc = recent_doc
			else:  # Create new tax exemption document
				doc.update({"doctype": doctype, "employee": emp})
			doc.update({
				"name": None,
				"amended_from": None,
				"docstatus": 0,
				"custom_yearly_bonus": 0,
				"declarations": []
			})
			frappe.get_doc(doc).insert()
			count += 1
			if publish_progress:
				frappe.publish_progress(
					count * 100 / len(emp_to_create),
					title=_("Creating Employee Tax Exemption Document..."),
				)
			frappe.db.commit()
		payroll_period.db_set({"custom_error_message": "", "custom_status": ""})
		return count
	except Exception as e:
		frappe.db.rollback()
		log_period_failure("creation", payroll_period, e)
	finally:
		frappe.db.commit()  # nosemgrep
		frappe.publish_realtime("completed_tax_exemption_creation", user=frappe.session.user)


def log_period_failure(process, payroll_period, error):
	error_log = frappe.log_error(
		title=_("Employee Tax Exemption Document {0} failed for Payroll Period {1}").format(process, payroll_period.name)
	)
	message_log = frappe.message_log.pop() if frappe.message_log else str(error)
	try:
		if isinstance(message_log, str):
			error_message = json.loads(message_log).get("message")
		else:
			error_message = message_log.get("message")
	except Exception:
		error_message = message_log
	error_message += "\n" + _("Check Error Log {0} for more details.").format(
		get_link_to_form("Error Log", error_log.name)
	)
	payroll_period.db_set({"custom_error_message": error_message, "custom_status": "Failed"})
