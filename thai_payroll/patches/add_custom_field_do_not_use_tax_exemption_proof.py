
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    custom_fields = {
        "Company": [
            {
                "fieldname": "do_not_use_tax_exemption_proof",
                "fieldtype": "Check",
                "label": "Do not use Tax Exemption Proof",
                "description": "Always use normal Emloyee Exemption Declaration "
                "even on last period salary and disregard Tax Exemption Proof.",
                "insert_after": "no_salary_recompute_on_submit"
            }
        ],
    }
    create_custom_fields(custom_fields, ignore_validate=True)
