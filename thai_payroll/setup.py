import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import (
    make_property_setter,
    delete_property_setter
)
from frappe.desk.page.setup_wizard.setup_wizard import make_records
from thai_payroll.constants import CUSTOM_FIELDS, PROPERTY_SETTERS


def after_install():
	create_custom_fields(CUSTOM_FIELDS, ignore_validate=True)
	create_property_setters()
	make_fixtures()
	update_severance_pay_settings()


# def after_migrate():
# 	create_custom_fields(CUSTOM_FIELDS, ignore_validate=True)
# 	create_property_setters()


def before_uninstall():
	delete_custom_fields(CUSTOM_FIELDS)
	delete_property_setters()


def create_property_setters():
	for doctypes, property_setters in PROPERTY_SETTERS.items():
		if isinstance(doctypes, str):
			doctypes = (doctypes,)
		for doctype in doctypes:
			for property_setter in property_setters:
				for_doctype = not property_setter[0]
				make_property_setter(doctype, *property_setter, for_doctype)


def delete_property_setters():
	for doctypes, property_setters in PROPERTY_SETTERS.items():
		if isinstance(doctypes, str):
			doctypes = (doctypes,)
		for doctype in doctypes:
			for property_setter in property_setters:
				delete_property_setter(doctype, property_setter[0])



def make_fixtures():
	records = [
		# Income Tax Slabs
		{
			"allow_tax_exemption": 1,
			"currency": "THB",
			"doctype": "Income Tax Slab",
			"effective_from": "2023-01-01",
			"name": "Thai PIT (2556)",
			"slabs": [
				{
					"from_amount": 0.0,
					"percent_deduction": 0.0,
					"to_amount": 150000.0
				},
				{
					"from_amount": 150001.0,
					"percent_deduction": 5.0,
					"to_amount": 300000.0
				},
				{
					"from_amount": 300001.0,
					"percent_deduction": 10.0,
					"to_amount": 500000.0
				},
				{
					"from_amount": 500001.0,
					"percent_deduction": 15.0,
					"to_amount": 750000.0
				},
				{
					"from_amount": 750001.0,
					"percent_deduction": 20.0,
					"to_amount": 1000000.0
				},
				{
					"from_amount": 1000001.0,
					"percent_deduction": 25.0,
					"to_amount": 2000000.0
				},
				{
					"from_amount": 2000001.0,
					"percent_deduction": 30.0,
					"to_amount": 5000000.0
				},
				{
					"from_amount": 5000001.0,
					"percent_deduction": 35.0,
					"to_amount": 0.0
				}
			]
		},
		{
			"allow_tax_exemption": 1,
			"currency": "THB",
			"doctype": "Income Tax Slab",
			"effective_from": "2023-01-01",
			"name": "Thai PIT for Severance Pay (2556)",
			"slabs": [
				{
					"from_amount": 0.0,
					"percent_deduction": 5.0,
					"to_amount": 300000.0
				},
				{
					"from_amount": 300001.0,
					"percent_deduction": 10.0,
					"to_amount": 500000.0
				},
				{
					"from_amount": 500001.0,
					"percent_deduction": 15.0,
					"to_amount": 750000.0
				},
				{
					"from_amount": 750001.0,
					"percent_deduction": 20.0,
					"to_amount": 1000000.0
				},
				{
					"from_amount": 1000001.0,
					"percent_deduction": 25.0,
					"to_amount": 2000000.0
				},
				{
					"from_amount": 2000001.0,
					"percent_deduction": 30.0,
					"to_amount": 5000000.0
				},
				{
					"from_amount": 5000001.0,
					"percent_deduction": 35.0,
					"to_amount": 0.0
				}
			]
		}
	]
	make_records(records)


def update_severance_pay_settings():
	settings = frappe.get_doc("Severance Pay Settings")
	settings.income_tax_slab = "Thai PIT for Severance Pay (2556)"
	settings.append("severance_pay_rates", {"working_years": 0, "working_days": 120, "months": 1})
	settings.append("severance_pay_rates", {"working_years": 1, "working_days": 0, "months": 3})
	settings.append("severance_pay_rates", {"working_years": 3, "working_days": 0, "months": 6})
	settings.append("severance_pay_rates", {"working_years": 6, "working_days": 0, "months": 8})
	settings.append("severance_pay_rates", {"working_years": 10, "working_days": 0, "months": 10})
	settings.append("severance_pay_rates", {"working_years": 20, "working_days": 0, "months": 14})
	settings.save()


def delete_custom_fields(custom_fields: dict):
	for doctype, fields in custom_fields.items():
		frappe.db.delete(
			"Custom Field",
			{
				"fieldname": ("in", [field["fieldname"] for field in fields]),
				"dt": doctype,
			},
		)
		frappe.clear_cache(doctype=doctype)