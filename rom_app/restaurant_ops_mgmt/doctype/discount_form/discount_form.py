import frappe
from frappe.model.document import Document
from datetime import datetime


class DiscountForm(Document):
    def validate(self):
        current_date = datetime.today().date()
        doc_save_date = datetime.strptime(self.date, '%Y-%m-%d').date()
        if (current_date > doc_save_date):
            frappe.throw("Editing records from the past is not permitted")
