import frappe
from frappe.model.document import Document
from datetime import datetime


class OpClosingChecklist(Document):
    def before_insert(self):
        branch = self.branch
        user_name = self.user_name
        current_date = datetime.today().date()
        rec_count = self.get_the_record_count(branch, user_name, current_date)
        if (rec_count > 0):
            frappe.throw("You are limited to adding just one record per day.")

    # def on_update(self):
    #     current_date = datetime.today().date()
    #     doc_save_date = datetime.strptime(self.date, '%Y-%m-%d').date()
    #     if (current_date == doc_save_date):
    #         pass
    #     else:
    #         frappe.throw("Editing records from the past is not permitted")

    def get_the_record_count(self, branch, user_name, date_obj):
        rec_count = frappe.db.count(self.doctype, filters={
            'user_name': user_name,
            'branch': branch,
            'date': date_obj
        })
        return rec_count
