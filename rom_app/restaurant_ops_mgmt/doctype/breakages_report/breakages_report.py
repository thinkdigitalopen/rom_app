import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.utils import date_diff


class BreakagesReport(Document):
    def before_save(self):
        doc_date = self.date
        current_date = datetime.today().date()
        date_difference = date_diff(current_date, doc_date)
        if (date_difference > 7):
            frappe.throw("You cannot save the record with a past date")
        if (date_difference < 0):
            frappe.throw("You shouldn't save the record with a future date")
