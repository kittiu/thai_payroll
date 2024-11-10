import frappe

def execute():
    # Remove old fields
    frappe.db.delete("Custom Field", {
        "name": ["in", [
            "Company-custom_email_template_for_employee_tax_exempt_declaration",
            "Employee Tax Exemption Declaration-custom_invest_in_auunity"
        ]]
    })
