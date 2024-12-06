import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.utils import date_diff


class ChefProduction(Document):
    def before_save(self):
        doc_date = self.date
        current_date = datetime.today().date()
        date_difference = date_diff(current_date, doc_date)
        if (date_difference > 7):
            frappe.throw("You cannot save the record with a past date")
        if (date_difference < 0):
            frappe.throw("You shouldn't save the record with a future date")

def update_totals(doc, method):
    """
    Calculate and update totals for wastage_amount in briyani and chicken categories.
    """
    # Calculate total wastage amount for briyani category
    doc.briyani_category_wastage_amount = sum(
        (row.wastage_amount or 0) for row in (doc.get("briyani_category_list") or [])
    )

    # Calculate total wastage amount for chicken category
    doc.chicken_category_wastage_amount = sum(
        (row.wastage_amount or 0) for row in (doc.get("chicken_category_list") or [])
    )