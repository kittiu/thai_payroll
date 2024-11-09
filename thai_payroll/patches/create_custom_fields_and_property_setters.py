
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from thai_payroll.constants import CUSTOM_FIELDS
from thai_payroll.setup import create_property_setters

def execute():
    # Run for the first time migrator
    create_custom_fields(CUSTOM_FIELDS, ignore_validate=True)
    create_property_setters()
