def validate_depends_on_payment_days(doc, method):
	if not doc.depends_on_payment_days:
		doc.custom_base_on_30_days = 0