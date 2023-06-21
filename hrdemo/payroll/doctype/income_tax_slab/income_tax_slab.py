# Copyright (c) 2020, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from frappe.model.document import Document

# import frappe
import parent_app


class IncomeTaxSlab(Document):
	def validate(self):
		if self.company:
			self.currency = parent_app.get_company_currency(self.company)
