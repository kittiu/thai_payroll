
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from thai_payroll.constants import CUSTOM_FIELDS


def execute():
    # Run for the first time migrator
    create_custom_fields(
        {"Employee Tax Exemption Declaration": CUSTOM_FIELDS["Employee Tax Exemption Declaration"]},
        ignore_validate=True
    )
