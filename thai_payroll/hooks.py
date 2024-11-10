app_name = "thai_payroll"
app_title = "Thai Payroll"
app_publisher = "Kitti U."
app_description = "Payroll with Thailand\'s regulations"
app_email = "kittiu@ecosoft.co.th"
app_license = "mit"
required_apps = ["erpnext", "hrms"]


# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/thai_payroll/css/thai_payroll.css"
# app_include_js = "/assets/thai_payroll/js/thai_payroll.js"

# include js, css files in header of web template
# web_include_css = "/assets/thai_payroll/css/thai_payroll.css"
# web_include_js = "/assets/thai_payroll/js/thai_payroll.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "thai_payroll/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Salary Slip": "public/js/salary_slip.js",
	"Company": "public/js/company.js",
	"Employee": "public/js/employee.js",
	"Employee Tax Exemption Declaration": "public/js/employee_tax_exemption_declaration.js",
	"Payroll Period": "public/js/payroll_period.js",
}
doctype_list_js = {
	"Employee Tax Exemption Declaration": "public/js/employee_tax_exemption_declaration_list.js",
	"Salary Slip": "public/js/salary_slip_list.js",
}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "thai_payroll/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "thai_payroll.utils.jinja_methods",
# 	"filters": "thai_payroll.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "thai_payroll.install.before_install"
after_install = "thai_payroll.install.after_install"
# after_migrate = "thai_payroll.setup.after_migrate"

# Uninstallation
# ------------

before_uninstall = "thai_payroll.setup.before_uninstall"
# after_uninstall = "thai_payroll.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "thai_payroll.utils.before_app_install"
# after_app_install = "thai_payroll.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "thai_payroll.utils.before_app_uninstall"
# after_app_uninstall = "thai_payroll.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "thai_payroll.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
    "Salary Slip": "thai_payroll.custom.salary_slip.SalarySlipThaiPayroll",
    "Payroll Period": "thai_payroll.custom.payroll_period.PayrollPeriodThaiPayroll",
    "Employee Tax Exemption Declaration": "thai_payroll.custom.employee_tax_exemption_declaration.EmployeeTaxExemptionDeclarationThaiPayroll",
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Employee Tax Exemption Declaration": {
		"validate": "thai_payroll.custom.employee_tax_exemption_declaration.calculate_thai_tax_exemption",
        "before_update_after_submit": "thai_payroll.custom.employee_tax_exemption_declaration.calculate_thai_tax_exemption",
	},
    "Salary Slip": {
        "onload": "thai_payroll.custom.salary_slip.onload",
        "on_update": "thai_payroll.custom.salary_slip.update_payroll_period",
        "on_submit": "thai_payroll.custom.salary_slip.update_last_submitted_slip",
        "on_cancel": "thai_payroll.custom.salary_slip.update_last_submitted_slip",
	},
    "Salary Component": {
		"validate": "thai_payroll.custom.salary_component.validate_depends_on_payment_days",
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"thai_payroll.tasks.all"
# 	],
# 	"daily": [
# 		"thai_payroll.tasks.daily"
# 	],
# 	"hourly": [
# 		"thai_payroll.tasks.hourly"
# 	],
# 	"weekly": [
# 		"thai_payroll.tasks.weekly"
# 	],
# 	"monthly": [
# 		"thai_payroll.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "thai_payroll.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "thai_payroll.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
override_doctype_dashboards = {
	"Payroll Period": "thai_payroll.custom.dashboard_overrides.get_dashboard_data_for_payroll_period",
}

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["thai_payroll.utils.before_request"]
# after_request = ["thai_payroll.utils.after_request"]

# Job Events
# ----------
# before_job = ["thai_payroll.utils.before_job"]
# after_job = ["thai_payroll.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"thai_payroll.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }


bulk_transaction_task_mapper = ["thai_payroll.custom.bulk_transaction.get_task_mapper"]
