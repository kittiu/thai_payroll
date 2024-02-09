import json
from ast import literal_eval

import frappe
import urllib3
from frappe import _
from frappe.model.meta import get_field_precision
from frappe.utils import flt

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
	doc.custom_total_fathermother_exemption = (
		int(doc.custom_own_fathermother_exemption or 0) * 30000
		+ int(doc.custom_spouse_fathermother_exemption or 0) * 30000
	)
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
	# Investments, total combined <= 500,000
	invests = {
		"custom_pvd_contribution": 0.15 * (doc.custom_total_yearly_income or 0),
		"custom_invest_in_rmf": 0.3 * (doc.custom_total_yearly_income or 0),
		"custom_invest_in_ssf": 0.3 * (doc.custom_total_yearly_income or 0),
		"custom_invest_in_auunity": 132000
	}
	total_invest = 0
	invest_keys = list(invests.keys())
	for i in invest_keys:
		doc.set(i, min(doc.get(i) or 0, invests[i]))
		total_invest += doc.get(i)
	invest_keys.reverse()
	diff = total_invest - 500000
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
		doc.custom_pvd_contribution,
		doc.custom_invest_in_rmf,
		doc.custom_invest_in_ssf,
		doc.custom_invest_in_auunity,
		doc.custom_social_security,
		doc.custom_compensation_by_labor_law,
		doc.custom_life_insurance,
		doc.custom_health_insurance,
		doc.custom_health_insurance_for_parents,
		doc.custom_invest_in_thai_esg
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


def salary_slip_onload(doc, method):
	wht_cert = frappe.get_all(
		"Withholding Tax Cert Employee",
		filters={"voucher_type": "Salary Slip","voucher_no": doc.name}
	)
	if wht_cert:
		doc.set_onload("wht_cert", wht_cert[0].name)

@frappe.whitelist()
def make_withholding_tax_cert_employee(doc):
	sal = json.loads(doc)
	cert = frappe.new_doc("Withholding Tax Cert Employee")
	cert.employee = sal["employee"]
	employee = frappe.get_doc("Employee", cert.employee)
	cert.employee_name = employee and employee.employee_name or ""
	cert.employee_tax_id = employee and employee.pan_number or ""
	cert.employee_address = employee and employee.permanent_address or ""
	cert.voucher_type = "Salary Slip"
	cert.voucher_no = sal["name"]
	cert.company_address = frappe.db.get_value(
		"Company", sal["company"], "custom_company_address_on_withholding_tax_cert"
	)
	cert.income_tax_form = "PND1"
	cert.date = sal["end_date"]
	cert.append(
		"withholding_tax_items",
		{
			"type_of_income": "1",
			"description": "เงินเดือน ค่าจ้าง ฯลฯ 40(1)",
			"tax_base": sal["ctc"],
			"tax_amount": sal["total_income_tax"],
		},
	)
	return cert


# @frappe.whitelist()
# def get_withholding_tax_employee(filters, doc):
	# filters = literal_eval(filters)
	# pay = json.loads(doc)
	# wht = frappe.get_doc("Withholding Tax Type", filters["wht_type"])
	# company = frappe.get_doc("Company", pay["company"])
	# base_amount = 0
	# for ref in pay.get("references"):
	# 	if ref.get("reference_doctype") not in [
	# 			"Purchase Invoice",
	# 			"Expense Claim",
	# 			"Journal Entry"
	# 		]:
	# 		return
	# 	if not ref.get("allocated_amount") or not ref.get("total_amount"):
	# 		continue
	# 	# Find gl entry of ref doc that has undue amount
	# 	gl_entries = frappe.db.get_all(
	# 		"GL Entry",
	# 		filters={
	# 			"voucher_type": ref["reference_doctype"],
	# 			"voucher_no": ref["reference_name"],
	# 		},
	# 		fields=[
	# 			"name",
	# 			"account",
	# 			"debit",
	# 			"credit",
	# 		],
	# 	)
	# 	for gl in gl_entries:
	# 		credit = gl["credit"]
	# 		debit = gl["debit"]
	# 		alloc_percent = ref["allocated_amount"] / ref["total_amount"]
	# 		report_type = frappe.get_cached_value("Account", gl["account"], "report_type")
	# 		if report_type == "Profit and Loss":
	# 			base_amount += alloc_percent * (credit - debit)
	# return {
	# 	# "account": wht.account,
	# 	# "cost_center": company.cost_center,
	# 	# "base": base_amount,
	# 	# "rate": wht.percent,
	# 	"amount": 
	# }
