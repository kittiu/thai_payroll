import frappe


def execute():
    rule_doc = frappe.get_doc({
        "doctype": "Income Tax Exemption Rule",
        "payroll_period": "2024",
        "child_born_before_2561": 30000.0,
        "child_born_from_2561": 60000.0,
        "compensation_by_labor_law": 300000.0,
        "disable_person_exemption": 190000.0,
        "disable_person_support": 60000.0,
        "doctype": "Income Tax Exemption Rule",
        "donation_for_political_party": 10000.0,
        "elderly_exemption": 190000.0,
        "elderly_spouse_exemption": 190000.0,
        "exemption": 60000.0,
        "expense": 100000.0,
        "health_insurance": 25000.0,
        "health_insurance_for_parents": 15000.0,
        "interest_paid_for_housing_loan": 100000.0,
        "invest_in_thai_esg": 300000.0,
        "life_insurance": 100000.0,
        "maternity_expense": 60000.0,
        "own_father_exemption": 30000.0,
        "own_mother_exemption": 30000.0,
        "pension_life_insurance": 200000.0,
        "social_security": 9000.0,
        "spouse_exemption": 60000.0,
        "spouse_father_exemption": 30000.0,
        "spouse_life_insurance": 10000.0,
        "spouse_mother_exemption": 30000.0,
        "total_contribution": 500000.0
    })
    rule_doc.save(ignore_permissions=True)
    return