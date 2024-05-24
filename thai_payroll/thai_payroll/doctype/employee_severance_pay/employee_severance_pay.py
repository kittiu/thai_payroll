# Copyright (c) 2024, Kitti U. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from hrms.payroll.doctype.salary_slip.salary_slip import calculate_tax_by_tax_slab
from frappe.utils import (
	add_days,
	add_years,
	add_months,
	cint,
	date_diff,
	flt,
	get_first_day,
	get_last_day,
	get_link_to_form,
	getdate,
	rounded,
	today,
)
from dateutil.relativedelta import relativedelta
import operator



class EmployeeSeverancePay(Document):

	def validate(self):
		# compute working year
		last_ss = self._get_last_salary_slip()
		self._validate_employee(last_ss)
		ss = frappe.get_doc("Salary Slip", last_ss)
		ss.set_salary_structure_assignment()
		self._compute_working_years()
		self._compute_income_expense(ss)
		self._compute_tax_amount()

	def _get_last_salary_slip(self):
		ss = frappe.get_all(
			"Salary Slip",
			filters={
				"docstatus": 1,
				"employee": self.employee,
			},
			pluck="name",
			limit=1,
			order_by="end_date DESC",
		)
		return ss[0] if ss else None
		
	def _validate_employee(self, last_ss):
		if not self.relieving_date:
			frappe.throw(_("This employee no 'Relieving Date' set yet."))
		if not last_ss:
			frappe.throw(_("This employee has no history of 'Salary Slip'."))

	def _compute_working_years(self):
		# Compute working years, residiual days > 183 days is another year.
		date_of_joining = getdate(self.date_of_joining)
		relieving_date = getdate(self.relieving_date)
		effective_date = add_days(relieving_date, 1)
		work_years = self.diff_years = relativedelta(effective_date, date_of_joining).years
		full_years_date = add_years(date_of_joining, self.diff_years)
		self.diff_days = (effective_date - full_years_date).days
		if self.diff_days > 183:
			work_years += 1
		self.work_years = work_years

	def _compute_income_expense(self, salary_slip):
		# Calculate Severance Pay Rate
		settings = frappe.get_doc(
			"Severance Pay Settings", "Severance Pay Settings"
		)
		if not settings.severance_pay_rates:
			frappe.throw(_("Severance Pay Rates is not setup yet"))
		# Find months of severance from rate table
		rates = list(filter(lambda x: x.working_years <= self.diff_years, settings.severance_pay_rates))
		rates.sort(key=lambda x: x.working_years)
		if rates and self.diff_days < rates[-1].working_days:  # Check date
			rates.pop()
		self.severance_months = rates and rates[-1].months or 0
		
		ssa = salary_slip._salary_structure_assignment
		self.last_month_salary = ssa.base
		self.total_work_years_salary = self.last_month_salary * self.work_years
		self.first_expense = 	self.work_years * 7000

		self.severance_amount = self.severance_months * self.last_month_salary
		self.income_amount = self.severance_amount + (self.one_time_amount or 0)
		self.total_income_amount = self.income_amount - (self.deduction_amount or 0)

		if self.income_amount < self.total_work_years_salary:
			self.income_for_expense_calc = self.income_amount
		else:
			self.income_for_expense_calc = self.total_work_years_salary

		self.first_remaining = self.income_for_expense_calc - self.first_expense
		self.second_expense = self.first_remaining * 0.5
		self.total_expense_amount = self.first_expense + self.second_expense

		if not self.fill_net_income_manually:
			self.net_income = self.total_income_amount - self.total_expense_amount

	def _compute_tax_amount(self):
		tax_slab = frappe.get_cached_doc("Income Tax Slab", self.income_tax_slab)
		self.computed_tax_amount = calculate_tax_by_tax_slab(
			self.net_income, tax_slab, eval_locals={}
		)
