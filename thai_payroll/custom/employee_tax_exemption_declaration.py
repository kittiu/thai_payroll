import json
from ast import literal_eval

import frappe
import urllib3
from frappe import _
from frappe.model.meta import get_field_precision
from frappe.utils import flt
from hrms.payroll.report.income_tax_computation.income_tax_computation import IncomeTaxComputationReport
from hrms.payroll.doctype.payroll_entry.payroll_entry import get_start_end_dates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def set_default_use_thai_pit_calculation(doc, method):
	if not doc.custom_use_thai_pit_calculation:
		doc.custom_use_thai_pit_calculation = frappe.db.get_value(
			"Company", doc.company, "custom_use_thai_pit_calculation"
		) or 0


def calculate_thai_tax_exemption(doc, method):
	if not doc.custom_use_thai_pit_calculation:
		return
	# Total income per year
	doc.custom_total_yearly_income = (doc.custom_yearly_salary or 0) + (doc.custom_yearly_bonus or 0)
	# -- 1. Exemption for Personal and Family --
	total_personal_family = calc_total_personal_family(doc)
	# -- 2. Exemption for Savings, Investments and Insurances --
	total_saving_invest_insurance = calc_total_saving_invest_insurance(doc)
	# -- 3. Exemption from Housing and Government Policy --
	total_housing_gov_policy = calc_total_housing_gov_policy(doc)
	# -- 4. Exemption from Government Economic Stimulus --
	total_economic_stimulus = calc_total_economic_stimulus(doc)
	# Total exemption before donation
	# Expense (50% of total income bue not over 100,000)
	doc.custom_expense = min(0.5 * (doc.custom_total_yearly_income or 0), 100000)
	total_exemption = sum([
		total_personal_family,
		total_saving_invest_insurance,
		total_housing_gov_policy,
		total_economic_stimulus,
		doc.custom_expense
	])
	doc.custom_yearly_income_after_exemption = doc.custom_total_yearly_income - total_exemption
	if doc.custom_yearly_income_after_exemption < 0:
		doc.custom_yearly_income_after_exemption = 0
	# -- 5. Exemption from Donation --
	total_donation = calc_total_donation(doc)
	# Summary of Exemptions
	doc.custom_exemption_group_1 = total_personal_family
	doc.custom_exemption_group_2 = total_saving_invest_insurance
	doc.custom_exemption_group_3 = total_housing_gov_policy
	doc.custom_exemption_group_4 = total_economic_stimulus
	doc.custom_exemption_group_5 = total_donation
	doc.custom_total_exemption = sum([
		doc.custom_expense,
		doc.custom_exemption_group_1,
		doc.custom_exemption_group_2,
		doc.custom_exemption_group_3,
		doc.custom_exemption_group_4,
		doc.custom_exemption_group_5
	])
	# Finally create declaration lines
	doc.declarations = []
	doc.append(
		"declarations",
		{
			"exemption_sub_category": "Thai Tax Exemption",
			"exemption_category": "Thai PIT",
			"max_amount": 10000000,
			"amount": doc.custom_total_exemption,
		}
	)
	doc.validate()


def calc_total_personal_family(doc):
	# Personal Exemption, 60,000
	doc.custom_exemption = 60000
	# Spose Exemption
	doc.custom_spouse_exemption = doc.custom_spouse_exemption and 60000 or 0
	# Child in education, 30,000
	doc.custom_total_child_exemption = (
		int(doc.custom_child_born_before_2561 or 0) * 30000
		+ int(doc.custom_child_born_from_2561 or 0) * 60000
	)
	# Parents
	doc.custom_total_fathermother_exemption = sum([
		doc.custom_own_father_exemption,
		doc.custom_own_mother_exemption,
		doc.custom_spouse_father_exemption,
		doc.custom_spouse_mother_exemption
   ]) * 30000
	# Disable Person
	doc.custom_disable_person_support = doc.custom_disable_person_support and 60000 or 0
	return sum([
		doc.custom_exemption,
		doc.custom_spouse_exemption,
		doc.custom_total_child_exemption,
		doc.custom_total_fathermother_exemption,
		doc.custom_disable_person_support
	])


def calc_total_saving_invest_insurance(doc):
	# Total Custom Contribution combined must not over 15% of total income
	doc.custom_total_contribution = sum([
		doc.custom_pvd_contribution or 0,
		doc.custom_school_contribution or 0,
		doc.custom_gpf_contribution or 0
	])
	# Show warning if total contribution > 15% of total income
	if doc.custom_total_contribution > 0.15 * (doc.custom_total_yearly_income or 0):
		frappe.msgprint(_("All 3 contributions combined should not over 15% of total income"))
	# Investments, total combined <= 500,000
	invests = {
		"custom_total_contribution": 0.15 * (doc.custom_total_yearly_income or 0),
		"custom_invest_in_rmf": 0.3 * (doc.custom_total_yearly_income or 0),
		"custom_invest_in_ssf": 0.3 * (doc.custom_total_yearly_income or 0),
		"custom_invest_in_auunity": 132000,
		"custom_pension_life_insurance": min(0.15 * (doc.custom_pension_life_insurance or 0), 200000),
	}
	total_invest = 0
	invest_keys = list(invests.keys())
	for i in invest_keys:
		doc.set(i, min(doc.get(i) or 0, invests[i]))
		total_invest += doc.get(i)
	invest_keys.reverse()
	diff = total_invest - 500000  # 500,000 is the limit
	for i in invest_keys:
		if diff > 0:
			if diff > doc.get(i):
				diff -= doc.get(i)
				doc.set(i, 0)
			elif diff > 0:
				doc.set(i, doc.get(i) - diff)
				diff = 0
				break
	# Social Security
	doc.custom_social_security = min(doc.custom_social_security or 0, 9000)
	# Labor Law Compensation
	doc.custom_compensation_by_labor_law = min(doc.custom_compensation_by_labor_law or 0, 300000)
	# Insurances
	doc.custom_life_insurance = min(doc.custom_life_insurance or 0, 100000)
	doc.custom_spouse_life_insurance = min(doc.custom_spouse_life_insurance or 0, 10000)
	doc.custom_health_insurance = min(doc.custom_health_insurance or 0, 25000)
	if doc.custom_life_insurance + doc.custom_health_insurance > 100000:
		doc.custom_health_insurance = 100000 - doc.custom_life_insurance
	# Insurance for parents
	doc.custom_health_insurance_for_parents = min(doc.custom_health_insurance_for_parents or 0, 15000)
	# Thai ESG 30% of income and < 100000
	doc.custom_invest_in_thai_esg = min(
		doc.custom_invest_in_thai_esg or 0,
		0.3 * doc.custom_total_yearly_income,
		100000
	)
	return sum([
		doc.custom_total_contribution or 0,
		doc.custom_invest_in_rmf or 0,
		doc.custom_invest_in_ssf or 0,
		doc.custom_invest_in_auunity or 0,
		doc.custom_pension_life_insurance or 0,
		doc.custom_social_security or 0,
		doc.custom_compensation_by_labor_law or 0,
		doc.custom_maternity_expense or 0,
		doc.custom_life_insurance or 0,
		doc.custom_spouse_life_insurance or 0,
		doc.custom_health_insurance or 0,
		doc.custom_health_insurance_for_parents or 0,
		doc.custom_invest_in_thai_esg or 0
	])


def calc_total_housing_gov_policy(doc):
	# Interest for loan
	doc.custom_interest_paid_for_housing_loan = min(doc.custom_interest_paid_for_housing_loan or 0, 100000)
	# Donation political party
	doc.custom_donation_for_political_party = min(doc.custom_donation_for_political_party or 0, 10000)
	# Insurance, max 100,000
	return sum([
		doc.custom_interest_paid_for_housing_loan,
		doc.custom_donation_for_political_party
	])


def calc_total_economic_stimulus(doc):
	return doc.custom_economic_stimulus_allowance or 0


def calc_total_donation(doc):
	doc.custom_donation_for_education = min(
		doc.custom_donation_for_education or 0,
		0.1 * (doc.custom_yearly_income_after_exemption or 0)
	)
	doc.custom_other_donation = min(
		doc.custom_other_donation or 0,
		0.1 * (doc.custom_yearly_income_after_exemption or 0)
	)
	return sum([
		doc.custom_donation_for_education * 2,  # 2X for education
		doc.custom_other_donation
	])


@frappe.whitelist()
def get_employee_yearly_salary(company, payroll_period, employee):
	emp = frappe.get_cached_doc("Employee", employee)
	pp = frappe.get_cached_doc("Payroll Period", payroll_period)
	ss = frappe.new_doc("Salary Slip")
	ss.company = company
	ss.employee = employee
	ss.start_date = emp.date_of_joining if pp.start_date < emp.date_of_joining else pp.start_date
	ss.salary_structure = ss.check_sal_struct()
	ss.payroll_frequency = frappe.db.get_value(
		"Salary Structure", ss.salary_structure, "payroll_frequency"
	)
	ss.end_date = get_start_end_dates(
		ss.payroll_frequency, ss.start_date
	).end_date
	ss.process_salary_structure()
	return ss.ctc