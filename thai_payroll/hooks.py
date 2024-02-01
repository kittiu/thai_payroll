app_name = "thai_payroll"
app_title = "Thai Payroll"
app_publisher = "Kitti U."
app_description = "Payroll with Thailand\'s regulations"
app_email = "kittiu@ecosoft.co.th"
app_license = "mit"
required_apps = ["erpnext", "hrms"]

fixtures = [
	{
		"doctype": "Employee Tax Exemption Category",
		"filters": [["name", "in", ("Thai PIT",)]]
	},
	{
		"doctype": "Employee Tax Exemption Sub Category",
		"filters": [["name", "in", ("Thai Tax Exemption",)]]
	},
	{
		"doctype": "Custom Field",
		"filters": [
			[
				"name",
				"in",
				(
					"Company-custom_use_thai_pit_calculation",
					"Company-custom_thai_payroll",
					"Employee Tax Exemption Declaration-custom_column_break_se1vc",
					"Employee Tax Exemption Declaration-custom_column_break_ofxie",
					"Employee Tax Exemption Declaration-custom_exemption_group_5",
					"Employee Tax Exemption Declaration-custom_exemption_group_4",
					"Employee Tax Exemption Declaration-custom_exemption_group_3",
					"Employee Tax Exemption Declaration-custom_exemption_group_2",
					"Employee Tax Exemption Declaration-custom_exemption_group_1",
					"Employee Tax Exemption Declaration-custom_column_break_ajygm",
					"Employee Tax Exemption Declaration-custom_column_break_rzpq0",
					"Employee Tax Exemption Declaration-custom_yearly_total_exemption",
					"Employee Tax Exemption Declaration-custom_column_break_lacao",
					"Employee Tax Exemption Declaration-custom_exemption_from_donation",
					"Employee Tax Exemption Declaration-custom_exemption_from_government_economic_stimulus",
					"Employee Tax Exemption Declaration-custom_column_break_jbejz",
					"Employee Tax Exemption Declaration-custom_exemption_from_housing_and_government_policy",
					"Employee Tax Exemption Declaration-custom_compensation_by_labor_law",
					"Employee Tax Exemption Declaration-custom_column_break_eqffq",
					"Employee Tax Exemption Declaration-custom_use_thai_pit_calculation",
					"Employee Tax Exemption Declaration-custom_donation_for_political_party",
					"Employee Tax Exemption Declaration-custom_total_exemption",
					"Employee Tax Exemption Declaration-custom_yearly_income_after_exemption",
					"Employee Tax Exemption Declaration-custom_child_born_from_2561",
					"Employee Tax Exemption Declaration-custom_child_born_before_2561",
					"Employee Tax Exemption Declaration-custom_total_yearly_income",
					"Employee Tax Exemption Declaration-custom_column_break_p78nx",
					"Employee Tax Exemption Declaration-custom_yearly_bonus",
					"Employee Tax Exemption Declaration-custom_column_break_t2icj",
					"Employee Tax Exemption Declaration-custom_yearly_salary",
					"Employee Tax Exemption Declaration-custom_yearly_income",
					"Employee Tax Exemption Declaration-custom_column_break_9w5os",
					"Employee Tax Exemption Declaration-custom_other_donation",
					"Employee Tax Exemption Declaration-custom_economic_stimulus_allowance",
					"Employee Tax Exemption Declaration-custom_donation_for_education",
					"Employee Tax Exemption Declaration-custom_column_break_c59yc",
					"Employee Tax Exemption Declaration-custom_invest_in_thai_esg",
					"Employee Tax Exemption Declaration-custom_invest_in_auunity",
					"Employee Tax Exemption Declaration-custom_invest_in_ssf",
					"Employee Tax Exemption Declaration-custom_invest_in_rmf",
					"Employee Tax Exemption Declaration-custom_column_break_szhdn",
					"Employee Tax Exemption Declaration-custom_health_insurance_for_parents",
					"Employee Tax Exemption Declaration-custom_health_insurance",
					"Employee Tax Exemption Declaration-custom_life_insurance",
					"Employee Tax Exemption Declaration-custom_column_break_8ugeq",
					"Employee Tax Exemption Declaration-custom_interest_paid_for_housing_loan",
					"Employee Tax Exemption Declaration-custom_pvd_contribution",
					"Employee Tax Exemption Declaration-custom_pvd_housing_loan_insurance_investment_donations",
					"Employee Tax Exemption Declaration-custom_column_break_wmbpx",
					"Employee Tax Exemption Declaration-custom_disable_person_support",
					"Employee Tax Exemption Declaration-custom_total_fathermother_exemption",
					"Employee Tax Exemption Declaration-custom_spouse_fathermother_exemption",
					"Employee Tax Exemption Declaration-custom_own_fathermother_exemption",
					"Employee Tax Exemption Declaration-custom_column_break_p5f1h",
					"Employee Tax Exemption Declaration-custom_total_child_exemption",
					"Employee Tax Exemption Declaration-custom_spouse_exemption",
					"Employee Tax Exemption Declaration-custom_exemption",
					"Employee Tax Exemption Declaration-custom_expense",
					"Employee Tax Exemption Declaration-custom_expense_and_exemption",
					"Employee Tax Exemption Declaration-custom_tab_4",
                    "Employee Tax Exemption Declaration-custom_social_security",
				),
			]
		],
	},
]

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
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
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
# after_install = "thai_payroll.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "thai_payroll.uninstall.before_uninstall"
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

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Employee Tax Exemption Declaration": {
        "before_insert": "thai_payroll.custom.custom_api.set_default_use_thai_pit_calculation",
		"on_update": "thai_payroll.custom.custom_api.calculate_thai_tax_exemption",
	},
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
# override_doctype_dashboards = {
# 	"Task": "thai_payroll.task.get_dashboard_data"
# }

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

