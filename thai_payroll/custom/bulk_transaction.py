def get_task_mapper():
	from thai_payroll.custom import salary_slip
	mapper = {
		"Salary Slip": {
			"Withholding Tax Cert Employee": salary_slip.make_withholding_tax_cert_employee,
		},
	}
	return mapper