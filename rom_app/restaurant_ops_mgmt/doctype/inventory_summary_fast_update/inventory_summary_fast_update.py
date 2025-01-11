import frappe
from datetime import datetime
from frappe.utils import date_diff
from frappe.model.document import Document


class InventorySummaryFastUpdate(Document):
    def validate(self):
        update_date = self.update_date
        current_date = datetime.today().date()
        date_difference = date_diff(current_date, update_date)
        print('date_difference ', date_difference)
        if (date_difference > 60):
            frappe.throw("You cannot set update before 60 days")
        if (date_difference < 0):
            frappe.throw("You cannot set future date")


