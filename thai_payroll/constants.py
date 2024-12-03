CUSTOM_FIELDS = {
	"Company": [
		{
			"fieldname": "custom_thai_payroll",
			"fieldtype": "Tab Break",
			"label": "Thai Payroll",
			"insert_after": "default_operating_cost_account",
		},
		{
			"fieldname": "section_break_pit",
			"fieldtype": "Section Break",
			"insert_after": "custom_thai_payroll",
		},
		{
			"fieldname": "column_break_pit_tax_exemption_option",
			"fieldtype": "Column Break",
            "label": "Tax Exemptions",
			"insert_after": "section_break_pit",
		},
		{
			"fieldname": "custom_use_thai_pit_calculation",
			"fieldtype": "Check",
			"label": "Use Thai PIT Calculation",
    		"description": "Enable Thai PIT Calculation in Employee Tax Exemption Declaration",
			"insert_after": "column_break_pit_tax_exemption_option",
		},
		{
			"depends_on": "eval:doc.custom_use_thai_pit_calculation",
			"description": "Choose between Lor Yor 01 (ลย.01) or Employee Tax Exemption Declaration. "
            "Lor Yor 01 is aimed for employee to fill in their own tax exemption, if used, "
            "Employee Tax Exemption Declaration will be created when submit Lor Yor 01",
			"fieldname": "tax_exemption_doctype",
			"fieldtype": "Select",
			"insert_after": "custom_use_thai_pit_calculation",
			"label": "Enable mass creation of Tax Exemption Doctype from Payroll Period",
            "options": "\nLor Yor 01\nEmployee Tax Exemption Declaration",
		},
		{
			"depends_on": "eval:doc.custom_use_thai_pit_calculation",
			"description": "On create/update Employee Tax exemption Declaration, auto fetch latest information about yearly salary and contributions (i.e., PVD)",
			"fieldname": "custom_auto_get_latest_salary_for_tax_exemption",
			"fieldtype": "Check",
			"insert_after": "tax_exemption_doctype",
			"label": "Auto get latest salary and contributions for Tax Exemption",
		},
		{
			"depends_on": "eval:doc.custom_use_thai_pit_calculation",
			"description": "On create/update slary slip, auto create new revision of Employee Tax Exemption Declaration if yearly salary or year PVD contribution changes",
			"fieldname": "custom_auto_revise_tax_exemption_declaration",
			"fieldtype": "Check",
			"insert_after": "custom_auto_get_latest_salary_for_tax_exemption",
			"label": "Auto revise Tax Exemption Declaration",
		},
		{
			"fieldname": "custom_column_break_4lgs1",
			"fieldtype": "Column Break",
            "label": "Emailing",
			"insert_after": "custom_auto_revise_tax_exemption_declaration",
		},
		{
			"fieldname": "thai_payroll_email_sender",
			"fieldtype": "Link",
			"label": "Email Sender",
			"options": "Contact",
            "insert_after": "custom_column_break_4lgs1",
            "description": "Note: If the Email Sender is not specified, system will use email from default outgoing email account instead"
		},
		{
			"fieldname": "email_template_for_lor_yor_01",
			"fieldtype": "Link",
			"label": "Email Template for Lor Yor 01",
			"options": "Email Template",
            "description": "Allow mass email sending on Lor Yor 01 list view",
			"insert_after": "thai_payroll_email_sender"
		},
		{
			"fieldname": "email_template_for_tax_exempt_declaration",
			"fieldtype": "Link",
			"label": "Email Template for Employee Tax Exemption Declaration",
			"options": "Email Template",
            "description": "Allow mass email sending on Employee Tax Exemption Declaratoin list view",
			"insert_after": "email_template_for_lor_yor_01",
		},
        {
            "fieldname": "section_break_wht_cert_employee",
            "fieldtype": "Section Break",
            "label": "Employee Withholding Tax Cert.",
            "insert_after": "email_template_for_tax_exempt_declaration",
        },
		{
			"fieldname": "custom_company_address_on_withholding_tax_cert",
			"fieldtype": "Link",
			"label": "Company Address On Withholding Tax Cert",
			"options": "Address",
			"insert_after": "section_break_wht_cert_employee"
		},
        {
            "fieldname": "section_other_settings",
            "fieldtype": "Section Break",
            "label": "Other Settings",
            "insert_after": "custom_company_address_on_withholding_tax_cert",
        },
		{
			"fieldname": "no_salary_recompute_on_submit",
			"fieldtype": "Check",
			"label": "Do not recompute salary slip on submit",
			"description": "Submit salary slip should not recompute earnings and deductions (skip validate function). "
            "To ensure that once calculated as draft, it will not change on submit even employee info changes.",
			"insert_after": "section_other_settings"
		}
	],
	"Salary Slip": [
		{
			"fetch_from": "employee.status",
			"fieldname": "custom_employee_status",
			"fieldtype": "Data",
			"insert_after": "letter_head",
			"label": "Employee Status",
			"read_only": 1
		},
		{
			"depends_on": "eval:doc.custom_employee_status=='Left'",
			"description": "Allow processing salary slip for employee who has left organization",
			"fieldname": "custom_allow_salary_slip",
			"fieldtype": "Check",
			"insert_after": "custom_employee_status",
			"label": "Allow Salary Slip",
		},
		{
			"fieldname": "custom_payroll_period",
			"fieldtype": "Link",
			"insert_after": "end_date",
			"label": "Payroll Period",
			"options": "Payroll Period",
			"read_only": 1
		},
		{
			"fieldname": "custom_latest_slip",
			"fieldtype": "Check",
			"insert_after": "salary_slip_based_on_timesheet",
			"label": "Latest Submitted Slip for Payroll Period",
			"read_only": 1
		},
		{
			"fieldname": "custom_connections",
			"fieldtype": "Tab Break",
			"insert_after": "leave_details",
			"label": "Connections",
		}
	],
	"Salary Component": [
		{
			"depends_on": "eval:doc.depends_on_payment_days",
			"description": "When partial month, amount = monthly amount / 30 days * work days",
			"fieldname": "custom_base_on_30_days",
			"fieldtype": "Check",
			"insert_after": "depends_on_payment_days",
			"label": "Daily amount is based on 30 days / month",
		}
	],
	"Salary Structure Assignment": [
		{
			"fieldname": "custom_pvd_contribution_till_date",
			"fieldtype": "Currency",
			"insert_after": "tax_deducted_till_date",
			"label": "PVD Contribution Till Date",
			"options": "currency"
		}
	],
	"Salary Structure": [
		{
			"description": "This salary component is used in calculating the PVD Contribution on Employee Tax Exemption Calculation",
			"fieldname": "custom_pvd_component",
			"fieldtype": "Link",
			"insert_after": "conditions_and_formula_variable_and_example",
			"label": "PVD Component",
			"options": "Salary Component",
			"link_filters": "[[\"Salary Component\",\"type\",\"=\",\"Deduction\"]]"
		}
	],
	"Employee": [
		{
			"fieldname": "custom_citizen_id",
			"fieldtype": "Data",
			"insert_after": "status",
			"label": "Citizen ID",
		},
		{
			"fieldname": "custom_pvd_type",
			"fieldtype": "Link",
			"insert_after": "payroll_cost_center",
			"label": "PVD Type",
			"options": "PVD Type"
		},
		{
			"fieldname": "custom_pvd_company",
			"fieldtype": "Percent",
			"insert_after": "custom_pvd_type",
			"label": "PVD Company",
		},
		{
			"fieldname": "custom_pvd_employee",
			"fieldtype": "Percent",
			"insert_after": "custom_pvd_company",
			"label": "PVD Employee",
		},
		{
			"fieldname": "custom_severance_pay",
			"fieldtype": "Section Break",
			"insert_after": "encashment_date",
			"label": "Severance Pay",
		},
		{
			"fieldname": "custom_employee_severance_pay",
			"fieldtype": "Link",
			"insert_after": "custom_severance_pay",
			"label": "Employee Severance Pay",
			"options": "Employee Severance Pay",
			"permlevel": 2
		},
		{
			"fieldname": "custom_column_break_nnjsi",
			"fieldtype": "Column Break",
			"insert_after": "custom_employee_severance_pay",
		},
		{
			"fetch_from": "custom_employee_severance_pay.income_amount",
			"fieldname": "custom_severance_pay_amount",
			"fieldtype": "Float",
			"insert_after": "custom_column_break_nnjsi",
			"label": "Severance Pay Amount",
			"permlevel": 2,
			"read_only": 1
		},
		{
			"fieldname": "custom_column_break_zaf2m",
			"fieldtype": "Column Break",
			"insert_after": "custom_severance_pay_amount",
			"name": "Employee-custom_column_break_zaf2m"
		},
		{
			"fetch_from": "custom_employee_severance_pay.computed_tax_amount",
			"fieldname": "custom_severance_tax_amount",
			"fieldtype": "Float",
			"insert_after": "custom_column_break_zaf2m",
			"label": "Severance Tax Amount",
			"permlevel": 2,
			"read_only": 1
		}
	],
	"Payroll Period": [
		{
			"description": "The Opening Period is the first period as is moved from other system",
			"fieldname": "custom_is_opening_period",
			"fieldtype": "Check",
			"insert_after": "company",
			"label": "Is Opening Period",
		},
		{
			"depends_on": "eval:doc.custom_is_opening_period",
			"description": "This Opening Period Date will have impact on Thai PIT Calculation - Yearly Salary and PVD Contribution",
			"fieldname": "custom_opening_period_date",
			"fieldtype": "Date",
			"insert_after": "custom_is_opening_period",
			"label": "Opening Period Date",
			"mandatory_depends_on": "eval:doc.custom_is_opening_period",
		},
		{
			"fieldname": "custom_tab_3",
			"fieldtype": "Tab Break",
			"insert_after": "periods",
			"label": "Create - Tax Exemption Document",
		},
		{
			"description": "Show active employees and allow mass creation of Employee Tax Exemption Declarations if not already exists. Recent tax exemption will be used if avaliable.",
			"fieldname": "custom_filter_employees",
			"fieldtype": "Section Break",
			"insert_after": "custom_tab_3",
			"label": "Filter Employees",
		},
		{
			"fieldname": "custom_branch",
			"fieldtype": "Link",
			"insert_after": "custom_filter_employees",
			"label": "Branch",
			"options": "Branch"
		},
		{
			"fieldname": "custom_department",
			"fieldtype": "Link",
			"insert_after": "custom_branch",
			"label": "Department",
			"options": "Department"
		},
		{
			"fieldname": "custom_status",
			"fieldtype": "Select",
			"insert_after": "custom_department",
			"label": "Status",
			"options": "\nQueued\nFailed",
			"read_only": 1
		},
		{
			"fieldname": "custom_column_break_r7sls",
			"fieldtype": "Column Break",
			"insert_after": "custom_status",
		},
		{
			"fieldname": "custom_designation",
			"fieldtype": "Link",
			"insert_after": "custom_column_break_r7sls",
			"label": "Designation",
			"options": "Designation"
		},
		{
			"fieldname": "custom_grade",
			"fieldtype": "Link",
			"insert_after": "custom_designation",
			"label": "Grade",
			"options": "Employee Grade"
		},
		{
			"fieldname": "custom_number_of_employees",
			"fieldtype": "Int",
			"insert_after": "custom_grade",
			"label": "Number Of Employees",
			"read_only": 1
		},
		{
			"fieldname": "custom_section_break_mr4ch",
			"fieldtype": "Section Break",
			"insert_after": "custom_number_of_employees",
			"label": "Active Employees",
		},
		{
			"fieldname": "custom_employees",
			"fieldtype": "Table",
			"insert_after": "custom_section_break_mr4ch",
			"label": "Tax Exemption Declaration will be created for employee not already has it",
			"options": "Payroll Period Employees",
			"read_only": 1
		},
		{
			"fieldname": "custom_failure_details",
			"fieldtype": "Tab Break",
			"insert_after": "custom_employees",
			"label": "Failure Details",
		},
		{
			"depends_on": "eval:doc.custom_status=='Failed';",
			"fieldname": "custom_error_message",
			"fieldtype": "Small Text",
			"insert_after": "custom_failure_details",
			"label": "Error Message",
			"read_only": 1
		}
	],
    "Employee Tax Exemption Declaration Category": [
        {
            "fieldname": "custom_input_amount",
            "fieldtype": "Currency",
            "in_list_view": 1,
            "insert_after": "max_amount",
            "label": "Input Amount",
            "options": "currency",
        },
	],
    "Employee Tax Exemption Declaration": [
        {
            "description": "Based on setting in Company's Thai Payroll",
            "fetch_from": "company.custom_use_thai_pit_calculation",
            "fieldname": "custom_use_thai_pit_calculation",
            "fieldtype": "Check",
            "insert_after": "department",
            "label": "Use Thai PIT Calculation on Tax Exemption",
        },
        {
            "depends_on": "eval:doc.custom_use_thai_pit_calculation",
            "description": "This Tax Exemption Declaration is the first entry as is moved from other system. This ensure yearly salary is computed based on Opening Entry Date.",
            "fetch_from": "payroll_period.custom_is_opening_period",
            "fieldname": "custom_is_opening_entry",
            "fieldtype": "Check",
            "insert_after": "custom_use_thai_pit_calculation",
            "label": "Is Opening Entry",
        },
        {
            "depends_on": "eval:doc.custom_is_opening_entry",
            "fetch_from": "payroll_period.custom_opening_period_date",
            "fieldname": "custom_opening_entry_date",
            "fieldtype": "Date",
            "insert_after": "custom_is_opening_entry",
            "label": "Opening Entry Date",
            "mandatory_depends_on": "eval:doc.custom_is_opening_entry",
        },
		{
			"fieldname": "ref_lor_yor_01",
			"fieldtype": "Link",
			"insert_after": "currency",
			"label": "Reference: Lor Yor 01",
			"options": "Lor Yor 01",
            "read_only": 1,
            "no_copy": 1,
		},
        {
            "depends_on": "eval:doc.custom_use_thai_pit_calculation==1",
            "fieldname": "custom_tab_4",
            "fieldtype": "Tab Break",
            "insert_after": "amended_from",
            "label": "Thai PIT Calculation",
        },
        {
            "description": "เงินได้พึงประเมิน",
            "fieldname": "custom_yearly_income",
            "fieldtype": "Section Break",
            "insert_after": "custom_tab_4",
            "label": "Income",
        },
        {
            "description": "เงินเดือนรวมทั้งปี",
            "fieldname": "custom_yearly_salary",
            "fieldtype": "Float",
            "insert_after": "custom_yearly_income",
            "label": "Yearly Salary",
        },
        {
            "depends_on": "eval:doc.docstatus==0",
            "description": "Get most up to date yearly salary",
            "fieldname": "custom_get_yearly_salary",
            "fieldtype": "Button",
            "insert_after": "custom_yearly_salary",
            "label": "Get Yearly Salary",
        },
        {
            "description": "โบนัส/รายได้อื่นรวมทั้งปี",
            "fieldname": "custom_yearly_bonus",
            "fieldtype": "Float",
            "insert_after": "custom_get_yearly_salary",
            "label": "Yearly Bonus",
        },
        {
            "fieldname": "custom_column_break_t2icj",
            "fieldtype": "Column Break",
            "insert_after": "custom_yearly_bonus",
        },
        {
            "description": "ผู้มีเงินได้อายุ เกิน 65 ปีขึ้นไปได้รับยกเว้น แต่ไม่เกิน 190,000 บาท",
            "fieldname": "custom_elderly_exemption",
            "fieldtype": "Float",
            "insert_after": "custom_column_break_t2icj",
            "label": "- Elderly Exemption",
        },
        {
            "description": "คู่สมรสผู้มีเงินได้อายุเกิน 65 ปีขึ้นไปได้รับยกเว้น แต่ไม่เกิน 190,000 บาท",
            "fieldname": "custom_elderly_spouse_exemption",
            "fieldtype": "Float",
            "insert_after": "custom_elderly_exemption",
            "label": "- Elderly Spouse Exemption",
        },
        {
            "description": "ผู้มีเงินได้เป็นผุ้พิการและมีอายุไม่เกิน 65 ปีได้รับยกเว้น แต่ไม่เกิน 190,000 บาท",
            "fieldname": "custom_disable_person_exemption",
            "fieldtype": "Float",
            "insert_after": "custom_elderly_spouse_exemption",
            "label": "- Disable Person Exemption",
        },
        {
            "description": "เงินค่าชดเชยที่ได้รับตามกฎหมายแรงงานได้รับการยกเว้น แต่ไม่เกิน 300,000 บาท (กรณีนำมารวมคำนวณภาษี)",
            "fieldname": "custom_compensation_by_labor_law",
            "fieldtype": "Float",
            "insert_after": "custom_disable_person_exemption",
            "label": "- Compensation by Labor Law",
        },
        {
            "fieldname": "custom_column_break_p78nx",
            "fieldtype": "Column Break",
            "insert_after": "custom_compensation_by_labor_law",
        },
        {
            "description": "<b>= เงินได้พึงประเมินรวมทั้งปี</b>",
            "fieldname": "custom_total_yearly_income",
            "fieldtype": "Float",
            "insert_after": "custom_column_break_p78nx",
            "label": "<b>= Total Yearly Income</b>",
            "read_only": 1,
        },
        {
            "description": "กลุ่มที่ 1 สิทธิลดหย่อนส่วนตัวและครอบครัว",
            "fieldname": "custom_expense_and_exemption",
            "fieldtype": "Section Break",
            "insert_after": "custom_total_yearly_income",
            "label": "1. Exemption for Personal and Family",
        },
        {
            "description": "ค่าลดหย่อนส่วนตัว (60,000)",
            "fieldname": "custom_exemption",
            "fieldtype": "Float",
            "insert_after": "custom_expense_and_exemption",
            "label": "Personal Exemption",
            "read_only": 1,
        },
        {
            "description": "ลดหย่อนกรณีคู่สมรสไม่มีรายได้ (60,000)",
            "fieldname": "custom_spouse_exemption",
            "fieldtype": "Float",
            "insert_after": "custom_exemption",
            "label": "Spouse Exemption",
        },
        {
            "fieldname": "custom_column_break_p5f1h",
            "fieldtype": "Column Break",
            "insert_after": "custom_spouse_exemption",
        },
        {
            "description": "บุตรวัยเรียนเกิดก่อนปี พ.ศ. 2561",
            "fieldname": "custom_child_born_before_2561",
            "fieldtype": "Select",
            "insert_after": "custom_column_break_p5f1h",
            "label": "Child born before 2561",
            "options": "\n1\n2\n3\n4\n5\n6",
        },
        {
            "description": "บุตรวัยเรียนเกิดตั้งแต่ พ.ศ. 2561",
            "fieldname": "custom_child_born_from_2561",
            "fieldtype": "Select",
            "insert_after": "custom_child_born_before_2561",
            "label": "Child born from 2561",
            "options": "\n1\n2\n3\n4\n5\n6",
        },
        {
            "description": "บุตรวัยเรียนเกิดก่อนปี 2561 (คนละ 30,000)\nบุตรวัยเรียนเกิดในหรือหลัง 2561 (คนละ 60,000)\n",
            "fieldname": "custom_total_child_exemption",
            "fieldtype": "Float",
            "insert_after": "custom_child_born_from_2561",
            "label": "Total Child Exemption",
            "read_only": 1,
        },
        {
            "fieldname": "custom_column_break_wmbpx",
            "fieldtype": "Column Break",
            "insert_after": "custom_total_child_exemption",
        },
        {
            "fieldname": "custom_own_father_exemption",
            "fieldtype": "Check",
            "insert_after": "custom_column_break_wmbpx",
            "label": "Own Father Exemption",
        },
        {
            "description": "เลี้ยงดูบิดามารดากรณีไม่มีรายได้  ท่านละ 30,000",
            "fieldname": "custom_own_mother_exemption",
            "fieldtype": "Check",
            "insert_after": "custom_own_father_exemption",
            "label": "Own Mother Exemption",
        },
        {
            "fieldname": "custom_spouse_father_exemption",
            "fieldtype": "Check",
            "insert_after": "custom_own_mother_exemption",
            "label": "Spouse Father Exemption",
        },
        {
            "description": "เลี้ยงดูบิดามารดาของคู่สมรส กรณีคู่สมรสไม่มีรายได้ ท่านละ 30,000",
            "fieldname": "custom_spouse_mother_exemption",
            "fieldtype": "Check",
            "insert_after": "custom_spouse_father_exemption",
            "label": "Spouse Mother Exemption",
        },
        {
            "description": "รวมลดหย่อน บิดา/มารดา (มีอายุตั้งแต่ 60 ปีขึ้นไปและอยู่ในความอุปการะเลี้ยงดูของผู้มีเงินได้)",
            "fieldname": "custom_total_fathermother_exemption",
            "fieldtype": "Float",
            "insert_after": "custom_spouse_mother_exemption",
            "label": "Total Father-Mother Exemption",
            "read_only": 1,
        },
        {
            "fieldname": "custom_column_break_9w5os",
            "fieldtype": "Column Break",
            "insert_after": "custom_total_fathermother_exemption",
        },
        {
            "description": "เป็นผู้ดูแลในบัตรประจำตัวของคนพิการ (คนละ 60,000)",
            "fieldname": "custom_disable_person_support",
            "fieldtype": "Float",
            "insert_after": "custom_column_break_9w5os",
            "label": "Disable Person Support",
        },
        {
            "collapsible": 1,
            "description": "กลุ่มที่ 2 ค่าลดหย่อน/ยกเว้น ด้านการออม การลงทุน และประกัน",
            "fieldname": "custom_pvd_housing_loan_insurance_investment_donations",
            "fieldtype": "Section Break",
            "insert_after": "custom_disable_person_support",
            "label": "2. Exemption for Savings, Investments and Insurances",
        },
        {
            "fieldname": "custom_column_break_szhdn",
            "fieldtype": "Column Break",
            "insert_after": "custom_pvd_housing_loan_insurance_investment_donations",
        },
        {
            "description": "กองทุนสำรองเลี้ยงชีพ",
            "fieldname": "custom_pvd_contribution",
            "fieldtype": "Float",
            "insert_after": "custom_column_break_szhdn",
            "label": "PVD Contribution",
        },
        {
            "depends_on": "eval:doc.docstatus==0",
            "description": "Get most up to date yearly PVD contribution",
            "fieldname": "custom_get_yearly_pvd_contribution",
            "fieldtype": "Button",
            "insert_after": "custom_pvd_contribution",
            "label": "Get Yearly PVD Contribution",
        },
        {
            "description": "กองทุนสงเคราะห์ครูโรงเรียนเอกชน",
            "fieldname": "custom_school_contribution",
            "fieldtype": "Float",
            "insert_after": "custom_get_yearly_pvd_contribution",
            "label": "Private School Contribution",
        },
        {
            "description": "กองทุนบําเหน็จบํานาญข้าราชการ",
            "fieldname": "custom_gpf_contribution",
            "fieldtype": "Float",
            "insert_after": "custom_school_contribution",
            "label": "GPF Contribution",
        },
        {
            "description": "รวม 3 กองทุน ลดหย่อนตามที่จ่ายจริงแต่ไม่เกิน 15% ของเงินได้ที่ต้องเสียภาษี และรวมส่วนนี้ทั้งหมดไม่เกิน 500,000 บาท",
            "fieldname": "custom_total_contribution",
            "fieldtype": "Float",
            "insert_after": "custom_gpf_contribution",
            "label": "Total Contribution",
            "read_only": 1,
        },
        {
            "fieldname": "custom_column_break_c59yc",
            "fieldtype": "Column Break",
            "insert_after": "custom_total_contribution",
        },
        {
            "description": "กองทุนการออมแห่งชาติ ลดหย่อนได้ตามที่จ่ายจริง แต่ไม่เกิน 13,200 บาท ทั้งนี้ และรวมส่วนนี้ทั้งหมดไม่เกิน 500,000 บาท",
            "fieldname": "custom_invest_in_annuity",
            "fieldtype": "Float",
            "insert_after": "custom_column_break_c59yc",
            "label": "Invest in Auunity",
        },
        {
            "description": "ลดหย่อนตามที่จ่ายจริงแต่ไม่เกิน 30% ของเงินได้ และรวมส่วนนี้ทั้งหมดไม่เกิน 500,000 บาท",
            "fieldname": "custom_invest_in_rmf",
            "fieldtype": "Float",
            "insert_after": "custom_invest_in_annuity",
            "label": "Invest in RMF",
        },
        {
            "description": "ลดหย่อนตามที่จ่ายจริงแต่ไม่เกิน 30% ของเงินได้ และรวมส่วนนี้ทั้งหมดไม่เกิน 500,000 บาท",
            "fieldname": "custom_invest_in_ssf",
            "fieldtype": "Float",
            "insert_after": "custom_invest_in_rmf",
            "label": "Invest in SSF",
        },
        {
            "description": "ค่าเบี้ยประกันชีวิตแบบบำนาญ หักค่าลดหย่อนในอัตราร้อยละ 15 ของเงินได้ที่นำมาเสียภาษีเงินได้ในแต่ละปี แต่ไม่เกิน 200,000 บาทต่อปี\nและเมื่อรวมกับเงินสะสมเข้ากองทุนสำรองเลี้ยงชีพ เงินสะสมเข้ากองทุนบำเหน็จบำนาญข้าราชการ (กบข.) เงินสะสมเข้ากองทุนสงเคราะห์ตามกฎหมายว่าด้วยโรงเรียนเอกชน เงินที่ซื้อหน่วยลงทุนในกองทุนรวมเพื่อการเลี้ยงชีพ (RMF) และเงินสะสมเข้ากองทุนการออมแห่งชาติ ต้องไม่เกิน 500,000 บาท",
            "fieldname": "custom_pension_life_insurance",
            "fieldtype": "Float",
            "insert_after": "custom_invest_in_ssf",
            "label": "Pension Life Insurance",
        },
        {
            "fieldname": "custom_column_break_eqffq",
            "fieldtype": "Column Break",
            "insert_after": "custom_pension_life_insurance",
        },
        {
            "description": "เงินสมทบกองทุนประกันสังคม\n<br>- มาตรา 33 ได้ตามจำนวนที่จ่ายจริง แต่ไม่เกิน 9,000 บาท\n<br>- มาตรา 39 ได้ตามจำนวนที่จ่ายจริง แต่ไม่เกิน 5,184 บาท\n<br>- มาตรา 40 ทางเลือกที่ 1 ได้ตามจำนวนที่จ่ายจริง แต่ไม่เกิน 840 บาท ทางเลือกที่ 2 ได้ตามจำนวนที่จ่ายจริง แต่ไม่เกิน 1,200 บาท ทางเลือกที่ 3 ได้ตามจำนวนที่จ่ายจริง แต่ไม่เกิน 3,600 บาท",
            "fieldname": "custom_social_security",
            "fieldtype": "Float",
            "insert_after": "custom_column_break_eqffq",
            "label": "Social Security",
        },
        {
            "description": "ค่าฝากครรภ์และค่าคลอดบุตร หักค่าลดหย่อนเท่าที่จ่ายจริง แต่ละคราวไม่เกิน 60,000 บาท",
            "fieldname": "custom_maternity_expense",
            "fieldtype": "Float",
            "insert_after": "custom_social_security",
            "label": "Maternity Expense",
        },
        {
            "fieldname": "custom_column_break_8ugeq",
            "fieldtype": "Column Break",
            "insert_after": "custom_maternity_expense",
        },
        {
            "description": "ประกันชีวิต ตามที่จ่ายจริงแต่ไม่เกิน 100,000 บาท",
            "fieldname": "custom_life_insurance",
            "fieldtype": "Float",
            "insert_after": "custom_column_break_8ugeq",
            "label": "Life Insurance",
        },
        {
            "description": "ประกันชีวิตคู่สมรส ตามที่จ่ายจริงแต่ไม่เกิน 10,000 บาท",
            "fieldname": "custom_spouse_life_insurance",
            "fieldtype": "Float",
            "insert_after": "custom_life_insurance",
            "label": "Spouse Life Insurance",
        },
        {
            "description": "ประกันสุขภาพ ตามที่จ่ายจริง แต่ไม่เกิน 25,000 บาท\nเมื่อรวมกับเบี้ยประกันชีวิตแล้วจะต้องไม่เกิน 100,000 บาท",
            "fieldname": "custom_health_insurance",
            "fieldtype": "Float",
            "insert_after": "custom_spouse_life_insurance",
            "label": "Health Insurance",
        },
        {
            "description": "จ่ายค่าประกันสุขภาพ บิดา/มารดาของตน และบิดา/มารดา ของคู่สมรสที่ไม่มีเงินได้ ให้ได้รับยกเว้นตามจำนวนที่จ่ายจริง แต่ไม่เกิน 15,000 บาท",
            "fieldname": "custom_health_insurance_for_parents",
            "fieldtype": "Float",
            "insert_after": "custom_health_insurance",
            "label": "Health Insurance for Parents",
        },
        {
            "description": "ลดหย่อนตามที่จ่ายจริงแต่ไม่เกิน 30% ของเงินได้ที่ต้องเสียภาษี และไม่เกิน 100,000 บาท สำหรับปีภาษีที่มีการลงทุน",
            "fieldname": "custom_invest_in_thai_esg",
            "fieldtype": "Float",
            "insert_after": "custom_health_insurance_for_parents",
            "label": "Invest in Thai ESG",
        },
        {
            "collapsible": 1,
            "description": "กลุ่มที่ 3 ค่าลดหย่อน/ยกเว้น จากสินทรัพย์และมาตรการนโยบายภาครัฐ",
            "fieldname": "custom_exemption_from_housing_and_government_policy",
            "fieldtype": "Section Break",
            "insert_after": "custom_invest_in_thai_esg",
            "label": "3. Exemption from Housing and Government Policy",
        },
        {
            "description": "ดอกเบื้ยเงินกู้ที่อยู่อาศัย ตามจำนวนที่จ่ายจริงแต่ไม่เกิน 100,000 บาท",
            "fieldname": "custom_interest_paid_for_housing_loan",
            "fieldtype": "Float",
            "insert_after": "custom_exemption_from_housing_and_government_policy",
            "label": "Interest Paid for Housing Loan",
        },
        {
            "fieldname": "custom_column_break_jbejz",
            "fieldtype": "Column Break",
            "insert_after": "custom_interest_paid_for_housing_loan",
        },
        {
            "description": "เงินบริจาคพรรคการเมือง ตามจำนวนที่จ่ายจริงแต่ไม่เกิน 10,000 บาท",
            "fieldname": "custom_donation_for_political_party",
            "fieldtype": "Float",
            "insert_after": "custom_column_break_jbejz",
            "label": "Donation for Political Party",
        },
        {
            "collapsible": 1,
            "description": "กลุ่มที่ 4 ค่าลดหย่อนจากนโยบายกระตุ้นเศรษฐกิจภาครัฐ เช่น ช้อปดีมีคืน",
            "fieldname": "custom_exemption_from_government_economic_stimulus",
            "fieldtype": "Section Break",
            "insert_after": "custom_donation_for_political_party",
            "label": "4. Exemption from Government Economic Stimulus",
        },
        {
            "description": "ลดหย่อนจากการกระตุ้นเศรษฐกิจตามที่กฏหมายกำหนด",
            "fieldname": "custom_economic_stimulus_allowance",
            "fieldtype": "Float",
            "insert_after": "custom_exemption_from_government_economic_stimulus",
            "label": "Economic stimulus allowance",
        },
        {
            "collapsible": 1,
            "description": "กลุ่มที่ 5 เงินบริจาค",
            "fieldname": "custom_exemption_from_donation",
            "fieldtype": "Section Break",
            "insert_after": "custom_economic_stimulus_allowance",
            "label": "5. Exemption from Donation",
        },
        {
            "description": "เงินได้สุทธิหลังหักค่าลดหย่อนและค่าใช้จ่าย",
            "fieldname": "custom_yearly_income_after_exemption",
            "fieldtype": "Float",
            "insert_after": "custom_exemption_from_donation",
            "label": "Yearly Income after Exemption",
            "read_only": 1,
        },
        {
            "fieldname": "custom_column_break_ofxie",
            "fieldtype": "Column Break",
            "insert_after": "custom_yearly_income_after_exemption",
        },
        {
            "description": "ลดหย่อน 2 เท่าของเงินที่จ่ายจริง แต่ไม่เกิน 10% ของเงินได้สุทธิ",
            "fieldname": "custom_donation_for_education",
            "fieldtype": "Float",
            "insert_after": "custom_column_break_ofxie",
            "label": "Donation for Education",
        },
        {
            "fieldname": "custom_column_break_lacao",
            "fieldtype": "Column Break",
            "insert_after": "custom_donation_for_education",
        },
        {
            "description": "ตามที่จ่ายจริง แต่ไม่เกิน 10% ของเงินได้สุทธิ",
            "fieldname": "custom_other_donation",
            "fieldtype": "Float",
            "insert_after": "custom_column_break_lacao",
            "label": "Other Donation",
        },
        {
            "fieldname": "custom_yearly_total_exemption",
            "fieldtype": "Section Break",
            "insert_after": "custom_other_donation",
            "label": "Yearly Total Exemption",
        },
        {
            "fieldname": "custom_column_break_rzpq0",
            "fieldtype": "Column Break",
            "insert_after": "custom_yearly_total_exemption",
        },
        {
            "description": "หักค่าใช้จ่าย 50% ของรายได้ทั้งปี (ไม่เกิน 100,000 บาท)",
            "fieldname": "custom_expense",
            "fieldtype": "Float",
            "insert_after": "custom_column_break_rzpq0",
            "label": "Expense",
            "read_only": 1,
        },
        {
            "fieldname": "custom_column_break_ajygm",
            "fieldtype": "Column Break",
            "insert_after": "custom_expense",
            "read_only": 1,
        },
        {
            "description": "กลุ่มที่ 1 สิทธิลดหย่อนส่วนตัวและครอบครัว",
            "fieldname": "custom_exemption_group_1",
            "fieldtype": "Float",
            "insert_after": "custom_column_break_ajygm",
            "label": "+ Exemption Group 1",
            "depends_on": "eval:doc.custom_exemption_group_1 > 0",
            "read_only": 1,
        },
        {
            "description": "กลุ่มที่ 2 ค่าลดหย่อน/ยกเว้น ด้านการออม การลงทุน และประกัน",
            "fieldname": "custom_exemption_group_2",
            "fieldtype": "Float",
            "insert_after": "custom_exemption_group_1",
            "label": "+ Exemption Group 2",
            "depends_on": "eval:doc.custom_exemption_group_2 > 0",
            "read_only": 1,
        },
        {
            "description": "กลุ่มที่ 3 ค่าลดหย่อน/ยกเว้น จากสินทรัพย์และมาตรการนโยบายภาครัฐ",
            "fieldname": "custom_exemption_group_3",
            "fieldtype": "Float",
            "insert_after": "custom_exemption_group_2",
            "label": "+ Exemption Group 3",
            "depends_on": "eval:doc.custom_exemption_group_3 > 0",
            "read_only": 1,
        },
        {
            "description": "กลุ่มที่ 4 ค่าลดหย่อนจากนโยบายกระตุ้นเศรษฐกิจภาครัฐ เช่น ช้อปดีมีคืน",
            "fieldname": "custom_exemption_group_4",
            "fieldtype": "Float",
            "insert_after": "custom_exemption_group_3",
            "label": "+ Exemption Group 4",
            "depends_on": "eval:doc.custom_exemption_group_4 > 0",
            "read_only": 1,
        },
        {
            "description": "กลุ่มที่ 5 เงินบริจาค",
            "fieldname": "custom_exemption_group_5",
            "fieldtype": "Float",
            "insert_after": "custom_exemption_group_4",
            "label": "+ Exemption Group 5",
            "depends_on": "eval:doc.custom_exemption_group_5 > 0",
            "read_only": 1,
        },
        {
            "fieldname": "custom_column_break_se1vc",
            "fieldtype": "Column Break",
            "insert_after": "custom_exemption_group_5",
        },
        {
            "description": "<b>= ค่าลดหย่อนทั้งหมด</b>",
            "fieldname": "custom_total_exemption",
            "fieldtype": "Float",
            "insert_after": "custom_column_break_se1vc",
            "label": "<b>= Total Exemption</b>",
            "bold": 1,
            "read_only": 1,
        }
    ]
}


PROPERTY_SETTERS = {
	"Salary Slip": [
		("custom_connections", "precision", "1", "Check"),
	],
    "Withholding Tax Cert Employee": [
        (None, "default_print_format", "Withholding Tax Cert Employee", "Data"),
    ],
    "Employee Tax Exemption Declaration Category": [
		(None, "field_order", "[\"exemption_sub_category\", \"exemption_category\", \"max_amount\", \"custom_input_amount\", \"amount\"]", "Data"),
		("max_amount", "in_list_view", "0", "Check"),
    ]
}
