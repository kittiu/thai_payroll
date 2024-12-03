
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from thai_payroll.constants import CUSTOM_FIELDS
from thai_payroll.setup import create_property_setters

def execute():
    # Update custom fields again, for field = no_salary_recompute_on_submit
    create_custom_fields(CUSTOM_FIELDS, ignore_validate=True)
