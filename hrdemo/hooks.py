from . import __version__ as app_version

app_name = "hrdemo"
app_title = "hr"
app_publisher = "hr"
app_description = "hr"
app_email = "hr"
app_license = "hr"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/hrdemo/css/hrdemo.css"
app_include_js = [
	"hrdemo.bundle.js",
	"performance.bundle.js",
]
app_include_css = "hrdemo.bundle.css"

# website

# include js, css files in header of web template
# web_include_css = "/assets/hrdemo/css/hrdemo.css"
# web_include_js = "/assets/hrdemo/js/hrdemo.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "hrdemo/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Employee": "public/js/parent_app/employee.js",
	"Company": "public/js/parent_app/company.js",
	"Department": "public/js/parent_app/department.js",
	"Timesheet": "public/js/parent_app/timesheet.js",
	"Payment Entry": "public/js/parent_app/payment_entry.js",
	"Journal Entry": "public/js/parent_app/journal_entry.js",
	"Delivery Trip": "public/js/parent_app/deliver_trip.js",
	"Bank Transaction": "public/js/parent_app/bank_transaction.js",
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

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
website_generators = ["Job Opening"]

website_route_rules = [
	{"from_route": "/jobs", "to_route": "Job Opening"},
]
# Jinja
# ----------

# add methods and filters to jinja environment
jinja = {
	"methods": [
		"hrdemo.utils.get_country",
	],
}

# Installation
# ------------

# before_install = "hrdemo.install.before_install"
after_install = "hrdemo.install.after_install"
after_migrate = "hrdemo.setup.update_select_perm_after_install"

# Uninstallation
# ------------

before_uninstall = "hrdemo.uninstall.before_uninstall"
# after_uninstall = "hrdemo.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "hrdemo.notifications.get_notification_config"

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

has_upload_permission = {
	"Employee": "parent_app.setup.doctype.employee.employee.has_upload_permission"
}

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Employee": "hrdemo.overrides.employee_master.EmployeeMaster",
	"Timesheet": "hrdemo.overrides.employee_timesheet.EmployeeTimesheet",
	"Payment Entry": "hrdemo.overrides.employee_payment_entry.EmployeePaymentEntry",
	"Project": "hrdemo.overrides.employee_project.EmployeeProject",
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"User": {
		"validate": "parent_app.setup.doctype.employee.employee.validate_employee_role",
		"on_update": "parent_app.setup.doctype.employee.employee.update_user_permissions",
	},
	"Company": {
		"validate": "hrdemo.overrides.company.validate_default_accounts",
		"on_update": [
			"hrdemo.overrides.company.make_company_fixtures",
			"hrdemo.overrides.company.set_default_hr_accounts",
		],
	},
	"Timesheet": {"validate": "hrdemo.hr.utils.validate_active_employee"},
	"Payment Entry": {
		"on_submit": "hrdemo.hr.doctype.expense_claim.expense_claim.update_payment_for_expense_claim",
		"on_cancel": "hrdemo.hr.doctype.expense_claim.expense_claim.update_payment_for_expense_claim",
		"on_update_after_submit": "hrdemo.hr.doctype.expense_claim.expense_claim.update_payment_for_expense_claim",
	},
	"Journal Entry": {
		"validate": "hrdemo.hr.doctype.expense_claim.expense_claim.validate_expense_claim_in_jv",
		"on_submit": [
			"hrdemo.hr.doctype.expense_claim.expense_claim.update_payment_for_expense_claim",
			"hrdemo.hr.doctype.full_and_final_statement.full_and_final_statement.update_full_and_final_statement_status",
		],
		"on_update_after_submit": "hrdemo.hr.doctype.expense_claim.expense_claim.update_payment_for_expense_claim",
		"on_cancel": [
			"hrdemo.hr.doctype.expense_claim.expense_claim.update_payment_for_expense_claim",
			"hrdemo.payroll.doctype.salary_slip.salary_slip.unlink_ref_doc_from_salary_slip",
			"hrdemo.hr.doctype.full_and_final_statement.full_and_final_statement.update_full_and_final_statement_status",
		],
	},
	"Loan": {"validate": "hrdemo.hr.utils.validate_loan_repay_from_salary"},
	"Employee": {
		"validate": "hrdemo.overrides.employee_master.validate_onboarding_process",
		"on_update": "hrdemo.overrides.employee_master.update_approver_role",
		"on_trash": "hrdemo.overrides.employee_master.update_employee_transfer",
	},
	"Project": {
		"validate": "hrdemo.controllers.employee_boarding_controller.update_employee_boarding_status"
	},
	"Task": {"on_update": "hrdemo.controllers.employee_boarding_controller.update_task"},
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"all": [
		"hrdemo.hr.doctype.interview.interview.send_interview_reminder",
	],
	"hourly": [
		"hrdemo.hr.doctype.daily_work_summary_group.daily_work_summary_group.trigger_emails",
	],
	"hourly_long": [
		"hrdemo.hr.doctype.shift_type.shift_type.process_auto_attendance_for_all_shifts",
	],
	"daily": [
		"hrdemo.controllers.employee_reminders.send_birthday_reminders",
		"hrdemo.controllers.employee_reminders.send_work_anniversary_reminders",
		"hrdemo.hr.doctype.daily_work_summary_group.daily_work_summary_group.send_summary",
		"hrdemo.hr.doctype.interview.interview.send_daily_feedback_reminder",
	],
	"daily_long": [
		"hrdemo.hr.doctype.leave_ledger_entry.leave_ledger_entry.process_expired_allocation",
		"hrdemo.hr.utils.generate_leave_encashment",
		"hrdemo.hr.utils.allocate_earned_leaves",
	],
	"weekly": ["hrdemo.controllers.employee_reminders.send_reminders_in_advance_weekly"],
	"monthly": ["hrdemo.controllers.employee_reminders.send_reminders_in_advance_monthly"],
}

advance_payment_doctypes = ["Gratuity", "Employee Advance"]

invoice_doctypes = ["Expense Claim"]

period_closing_doctypes = ["Payroll Entry"]

accounting_dimension_doctypes = [
	"Expense Claim",
	"Expense Claim Detail",
	"Expense Taxes and Charges",
	"Payroll Entry",
]

bank_reconciliation_doctypes = ["Expense Claim"]

# Testing
# -------

before_tests = "hrdemo.utils.before_tests"

# Overriding Methods
# -----------------------------

# get matching queries for Bank Reconciliation
get_matching_queries = "hrdemo.hr.utils.get_matching_queries"

regional_overrides = {
	"India": {
		"hrdemo.hr.utils.calculate_annual_eligible_hra_exemption": "hrdemo.regional.india.utils.calculate_annual_eligible_hra_exemption",
		"hrdemo.hr.utils.calculate_hra_exemption_for_period": "hrdemo.regional.india.utils.calculate_hra_exemption_for_period",
	},
}

# parent_app doctypes for Global Search
global_search_doctypes = {
	"Default": [
		{"doctype": "Salary Slip", "index": 19},
		{"doctype": "Leave Application", "index": 20},
		{"doctype": "Expense Claim", "index": 21},
		{"doctype": "Employee Grade", "index": 37},
		{"doctype": "Job Opening", "index": 39},
		{"doctype": "Job Applicant", "index": 40},
		{"doctype": "Job Offer", "index": 41},
		{"doctype": "Salary Structure Assignment", "index": 42},
		{"doctype": "Appraisal", "index": 43},
	],
}

# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "hrdemo.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
override_doctype_dashboards = {
	"Employee": "hrdemo.overrides.dashboard_overrides.get_dashboard_for_employee",
	"Holiday List": "hrdemo.overrides.dashboard_overrides.get_dashboard_for_holiday_list",
	"Task": "hrdemo.overrides.dashboard_overrides.get_dashboard_for_project",
	"Project": "hrdemo.overrides.dashboard_overrides.get_dashboard_for_project",
	"Timesheet": "hrdemo.overrides.dashboard_overrides.get_dashboard_for_timesheet",
}

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


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
# 	"hrdemo.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []
