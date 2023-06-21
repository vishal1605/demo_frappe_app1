import frappe

from hrdemo.overrides.company import make_salary_components, run_regional_setup


def execute():
	for country in frappe.get_all("Company", pluck="country", distinct=True):
		print("||||||||||||||||||||Start From Here||||||||||||||||")
		run_regional_setup(country)
		make_salary_components(country)
