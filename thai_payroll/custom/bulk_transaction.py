import frappe


def task(doc_name, from_doctype, to_doctype):
	from erpnext.accounts.doctype.payment_entry import payment_entry
	from erpnext.accounts.doctype.purchase_invoice import purchase_invoice
	from erpnext.accounts.doctype.sales_invoice import sales_invoice
	from erpnext.buying.doctype.purchase_order import purchase_order
	from erpnext.buying.doctype.supplier_quotation import supplier_quotation
	from erpnext.selling.doctype.quotation import quotation
	from erpnext.selling.doctype.sales_order import sales_order
	from erpnext.stock.doctype.delivery_note import delivery_note
	from erpnext.stock.doctype.purchase_receipt import purchase_receipt
	# Thai Base
	from thai_payroll.custom import salary_slip
	# --

	mapper = {
		"Sales Order": {
			"Sales Invoice": sales_order.make_sales_invoice,
			"Delivery Note": sales_order.make_delivery_note,
			"Payment Entry": payment_entry.get_payment_entry,
		},
		"Sales Invoice": {
			"Delivery Note": sales_invoice.make_delivery_note,
			"Payment Entry": payment_entry.get_payment_entry,
		},
		"Delivery Note": {
			"Sales Invoice": delivery_note.make_sales_invoice,
			"Packing Slip": delivery_note.make_packing_slip,
		},
		"Quotation": {
			"Sales Order": quotation.make_sales_order,
			"Sales Invoice": quotation.make_sales_invoice,
		},
		"Supplier Quotation": {
			"Purchase Order": supplier_quotation.make_purchase_order,
			"Purchase Invoice": supplier_quotation.make_purchase_invoice,
		},
		"Purchase Order": {
			"Purchase Invoice": purchase_order.make_purchase_invoice,
			"Purchase Receipt": purchase_order.make_purchase_receipt,
			"Payment Entry": payment_entry.get_payment_entry,
		},
		"Purchase Invoice": {
			"Purchase Receipt": purchase_invoice.make_purchase_receipt,
			"Payment Entry": payment_entry.get_payment_entry,
		},
		"Purchase Receipt": {"Purchase Invoice": purchase_receipt.make_purchase_invoice},
		# Thai Base
		"Salary Slip": {
			"Withholding Tax Cert Employee": salary_slip.make_withholding_tax_cert_employee,
		},
		# --
	}
	frappe.flags.bulk_transaction = True
	if to_doctype in ["Payment Entry"]:
		obj = mapper[from_doctype][to_doctype](from_doctype, doc_name)
	else:
		obj = mapper[from_doctype][to_doctype](doc_name)

	obj.flags.ignore_validate = True
	obj.set_title_field()
	obj.insert(ignore_mandatory=True)
	del frappe.flags.bulk_transaction