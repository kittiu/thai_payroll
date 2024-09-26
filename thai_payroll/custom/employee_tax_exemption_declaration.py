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
	# -- Exemption before calc total yearly income
	_total_first_exemption = calc_total_first_exemption(doc)
	# Total income per year
	doc.custom_total_yearly_income = sum([
		(doc.custom_yearly_salary or 0),
		(doc.custom_yearly_bonus or 0),
		-_total_first_exemption
	])
	# -- 1. Exemption for Personal and Family --
	_total_personal_family = calc_total_personal_family(doc)
	# -- 2. Exemption for Savings, Investments and Insurances --
	_total_saving_invest_insurance = calc_total_saving_invest_insurance(doc)
	# -- 3. Exemption from Housing and Government Policy --
	_total_housing_gov_policy = calc_total_housing_gov_policy(doc)
	# -- 4. Exemption from Government Economic Stimulus --
	_total_economic_stimulus = calc_total_economic_stimulus(doc)
	# Total exemption before donation
	# Expense (50% of total income bue not over 100,000)
	doc._custom_expense = min(0.5 * (doc.custom_total_yearly_income or 0), 100000)
	total_exemption = sum([
		_total_personal_family,
		_total_saving_invest_insurance,
		_total_housing_gov_policy,
		_total_economic_stimulus,
		doc._custom_expense
	])
	doc.custom_yearly_income_after_exemption = doc.custom_total_yearly_income - total_exemption
	if doc.custom_yearly_income_after_exemption < 0:
		doc.custom_yearly_income_after_exemption = 0
	# -- 5. Exemption from Donation --
	_total_donation = calc_total_donation(doc)
	# Summary of Exemptions
	doc.custom_expense = doc._custom_expense
	doc.custom_exemption_group_1 = _total_personal_family
	doc.custom_exemption_group_2 = _total_saving_invest_insurance
	doc.custom_exemption_group_3 = _total_housing_gov_policy
	doc.custom_exemption_group_4 = _total_economic_stimulus
	doc.custom_exemption_group_5 = _total_donation
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
	compute_exemption_declarations(doc)
	doc.validate()


def calc_total_first_exemption(doc):
	doc._custom_elderly_exemption = min((doc.custom_elderly_exemption or 0), 190000)
	doc._custom_elderly_spouse_exemption = min((doc.custom_elderly_spouse_exemption or 0), 190000)
	doc._custom_disable_person_exemption = min((doc.custom_disable_person_exemption or 0), 190000)
	doc._custom_compensation_by_labor_law = min((doc.custom_compensation_by_labor_law or 0), 300000)
	return sum([
		doc._custom_elderly_exemption,
		doc._custom_elderly_spouse_exemption,
		doc._custom_disable_person_exemption,
		doc._custom_compensation_by_labor_law
	])

def calc_total_personal_family(doc):
	# Personal Exemption, 60,000
	doc.custom_exemption = 60000
	doc._custom_exemption = doc.custom_exemption
	# Spose Exemption
	# doc.custom_spouse_exemption = doc.custom_spouse_exemption and 60000 or 0
	doc._custom_spouse_exemption = doc.custom_spouse_exemption and 60000 or 0
	# Child in education, 30,000
	doc.custom_total_child_exemption = (
		int(doc.custom_child_born_before_2561 or 0) * 30000
		+ int(doc.custom_child_born_from_2561 or 0) * 60000
	)
	doc._custom_total_child_exemption = doc.custom_total_child_exemption
	# Parents
	doc.custom_total_fathermother_exemption = sum([
		doc.custom_own_father_exemption,
		doc.custom_own_mother_exemption,
		doc.custom_spouse_father_exemption,
		doc.custom_spouse_mother_exemption
   ]) * 30000
	doc._custom_total_fathermother_exemption = doc.custom_total_fathermother_exemption
	# Disable Person
	# doc.custom_disable_person_support = doc.custom_disable_person_support and 60000 or 0
	doc._custom_disable_person_support = doc.custom_disable_person_support or 0
	return sum([
		doc._custom_exemption,
		doc._custom_spouse_exemption,
		doc._custom_total_child_exemption,
		doc._custom_total_fathermother_exemption,
		doc._custom_disable_person_support
	])


def calc_total_saving_invest_insurance(doc):
	# Total Custom Contribution combined must not over 15% of total income
	doc.custom_total_contribution = sum([
		doc.custom_pvd_contribution or 0,
		doc.custom_school_contribution or 0,
		doc.custom_gpf_contribution or 0
	])
	# Investments, total combined <= 500,000
	invests = {
		"custom_pvd_contribution": 0.15 * (doc.custom_total_yearly_income or 0),
		"custom_school_contribution": 0.15 * (doc.custom_total_yearly_income or 0),
		"custom_gpf_contribution": 0.15 * (doc.custom_total_yearly_income or 0),
		"custom_invest_in_rmf": 0.3 * (doc.custom_total_yearly_income or 0),
		"custom_invest_in_ssf": 0.3 * (doc.custom_total_yearly_income or 0),
		"custom_invest_in_auunity": 132000,
		"custom_pension_life_insurance": min(0.15 * (doc.custom_total_yearly_income or 0), 200000),
	}
	total_invest = 0
	invest_keys = list(invests.keys())
	for i in invest_keys:
		# Set _custom_invest...
		doc.set("_{}".format(i), min(doc.get(i) or 0, invests[i]))
		total_invest += doc.get("_{}".format(i))
	invest_keys.reverse()
	diff = total_invest - 500000  # 500,000 is the limit
	for i in invest_keys:
		if diff > 0:
			if diff > doc.get("_{}".format(i)):
				diff -= doc.get("_{}".format(i))
				doc.set("_{}".format(i), 0)
			elif diff > 0:
				doc.set("_{}".format(i), doc.get("_{}".format(i)) - diff)
				diff = 0
				break
	# Social Security
	doc._custom_social_security = min(doc.custom_social_security or 0, 9000)
	# Mothernity
	doc._custom_maternity_expense = doc.custom_maternity_expense or 0
	# Insurances
	doc._custom_life_insurance = min(doc.custom_life_insurance or 0, 100000)
	doc._custom_spouse_life_insurance = min(doc.custom_spouse_life_insurance or 0, 10000)
	doc._custom_health_insurance = min(doc.custom_health_insurance or 0, 25000)
	if doc._custom_life_insurance + doc._custom_health_insurance > 100000:
		doc._custom_health_insurance = 100000 - doc._custom_life_insurance
	# Insurance for parents
	doc._custom_health_insurance_for_parents = min(doc.custom_health_insurance_for_parents or 0, 15000)
	# Thai ESG 30% of income and < 100000
	doc._custom_invest_in_thai_esg = min(
		doc.custom_invest_in_thai_esg or 0,
		0.3 * doc.custom_total_yearly_income,
		100000
	)
	return sum([
		doc._custom_pvd_contribution or 0,
		doc._custom_school_contribution or 0,
		doc._custom_gpf_contribution or 0,
		doc._custom_invest_in_rmf or 0,
		doc._custom_invest_in_ssf or 0,
		doc._custom_invest_in_auunity or 0,
		doc._custom_pension_life_insurance or 0,
		doc._custom_social_security or 0,
		doc._custom_maternity_expense or 0,
		doc._custom_life_insurance or 0,
		doc._custom_spouse_life_insurance or 0,
		doc._custom_health_insurance or 0,
		doc._custom_health_insurance_for_parents or 0,
		doc._custom_invest_in_thai_esg or 0
	])


def calc_total_housing_gov_policy(doc):
	# Interest for loan
	doc._custom_interest_paid_for_housing_loan = min(doc.custom_interest_paid_for_housing_loan or 0, 100000)
	# Donation political party
	doc._custom_donation_for_political_party = min(doc.custom_donation_for_political_party or 0, 10000)
	# Insurance, max 100,000
	return sum([
		doc._custom_interest_paid_for_housing_loan,
		doc._custom_donation_for_political_party
	])


def calc_total_economic_stimulus(doc):
	doc._custom_economic_stimulus_allowance = doc.custom_economic_stimulus_allowance or 0
	return sum([
		doc._custom_economic_stimulus_allowance
	])


def calc_total_donation(doc):
	doc._custom_donation_for_education = min(
		doc.custom_donation_for_education or 0,
		0.1 * (doc.custom_yearly_income_after_exemption or 0)
	) * 2  # 2X for education
	doc._custom_other_donation = min(
		doc.custom_other_donation or 0,
		0.1 * (doc.custom_yearly_income_after_exemption or 0)
	)
	return sum([
		doc._custom_donation_for_education,
		doc._custom_other_donation
	])


EXEMPTIONS = {
	"หักเงินที่ได้รับการยกเว้น": {
		"ผู้มีเงินได้อายุเกิน 65 ปี ได้รับยกเว้น": "custom_elderly_exemption",
		"คู่สมรสผู้มีเงินได้อายุเกิน 65 ปีขึ้นไป ได้รับยกเว้น": "custom_elderly_spouse_exemption",
		"ผู้มีเงินได้เป็นผุ้พิการและมีอายุไม่เกิน 65 ปีบริบูรณ์": "custom_disable_person_exemption",
		"เงินชดเชยที่ได้รับตามกฎหมายแรงงาน": "custom_compensation_by_labor_law",
	},
	"หักค่าใช้จ่าย": {
		"หักค่าใช้จ่ายไม่เกิน 100,000 บาท": "custom_expense",
	},
	"กลุ่มที่ 1 สิทธิลดหย่อนส่วนตัวและครอบครัว": {
		"ค่าลดหย่อนส่วนตัว 60,000 บาท": "custom_exemption",
		"กรณีคู่สมรสไม่มีรายได้": "custom_spouse_exemption",
		"เลี้ยงดูบุตร": "custom_total_child_exemption",
		"เลี้ยงดูบิดามารดากรณีไม่มีรายได้": "custom_total_fathermother_exemption",
		"เป็นผู้ดูแลในบัตรประจำตัวของคนพิการ": "custom_disable_person_support",
	},
	"กลุ่มที่ 2 ค่าลดหย่อน/ยกเว้น ด้านการออม การลงทุน และประกัน": {
		"กองทุนสำรองเลี้ยงชีพ": "custom_pvd_contribution",
		"กองทุนสงเคราะห์ครูโรงเรียนเอกชน": "custom_school_contribution",
		"กองทุนบําเหน็จบํานาญข้าราชการ": "custom_gpf_contribution",
		"กองทุน RMF": "custom_invest_in_rmf", 
		"กองทุน SSF": "custom_invest_in_ssf",
		"กองทุนการออมแห่งชาติ": "custom_invest_in_auunity",
		"ค่าเบี้ยประกันชีวิตแบบบำนาญ": "custom_pension_life_insurance",
		"เงินสมทบกองทุนประกันสังคม": "custom_social_security",
		"ค่าฝากครรภ์และค่าคลอดบุตร": "custom_maternity_expense",
		"ประกันชีวิต": "custom_life_insurance",
		"ประกันชีวิตคู่สมรส": "custom_spouse_life_insurance",
		"ประกันสุขภาพ ": "custom_health_insurance",
		"จ่ายค่าประกันสุขภาพ บิดา/มารดา": "custom_health_insurance_for_parents",
		"กองทุน Thai ESG": "custom_invest_in_thai_esg",
	},
	"กลุ่มที่ 3 ค่าลดหย่อน/ยกเว้น จากสินทรัพย์และมาตรการนโยบายภาครัฐ": {
		"ดอกเบื้ยเงินกู้ที่อยู่อาศัย": "custom_interest_paid_for_housing_loan",
		"เงินบริจาคพรรคการเมือง": "custom_donation_for_political_party",
	},
	"กลุ่มที่ 4 ค่าลดหย่อนจากนโยบายกระตุ้นเศรษฐกิจภาครัฐ เช่น ช้อปดีมีคืน": {
		"ลดหย่อนจากการกระตุ้นเศรษฐกิจตามที่กฏหมายกำหนด": "custom_economic_stimulus_allowance",
	},
	"กลุ่มที่ 5 เงินบริจาค": {
		"บริจาคเพื่อการศึกษา (2 เท่า)": "custom_donation_for_education",
		"บริจาคอื่นๆ": "custom_other_donation",
	},
}


def compute_exemption_declarations(doc):
	create_exemption_categ()
	for categ in EXEMPTIONS.keys():
		for sub_categ in EXEMPTIONS[categ].keys():
			key = EXEMPTIONS[categ][sub_categ]
			doc.append(
				"declarations",
				{
					"exemption_sub_category": sub_categ,
					"exemption_category": categ,
					"max_amount": 999999999,
					"custom_input_amount": doc.get(key, 0),
					"amount": doc.get("_{}".format(key), 0),
				}
			)


def create_exemption_categ():
	# Create Exemption Categories if not already exists
	for categ in EXEMPTIONS.keys():
		doc = frappe.get_doc({
			"doctype": "Employee Tax Exemption Category",
			"name": categ,
		})
		doc.insert(ignore_permissions=True, ignore_if_duplicate=True)
		for sub_categ in EXEMPTIONS[categ].keys():
			doc = frappe.get_doc({
				"doctype": "Employee Tax Exemption Sub Category",
				"exemption_category": categ,
				"name": sub_categ,
			})
			doc.insert(ignore_permissions=True, ignore_if_duplicate=True)


@frappe.whitelist()
def get_employee_yearly_salary(company, payroll_period, employee):
	emp = frappe.get_cached_doc("Employee", employee)
	pp = frappe.get_cached_doc("Payroll Period", payroll_period)
	ss = frappe.new_doc("Salary Slip")
	ss.company = company
	ss.employee = employee
	ss.start_date = max(emp.date_of_joining, pp.start_date)
	ss.salary_structure = ss.check_sal_struct()
	if not ss.salary_structure:
		return 0
	ss.payroll_frequency = frappe.db.get_value(
		"Salary Structure", ss.salary_structure, "payroll_frequency"
	)
	date_detail = get_start_end_dates(
		ss.payroll_frequency, ss.start_date
	)
	ss.start_date = date_detail.start_date
	ss.end_date = date_detail.end_date
	ss.process_salary_structure()
	return ss.ctc
