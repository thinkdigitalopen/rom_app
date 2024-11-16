import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.utils import date_diff


class SalesReport(Document):
    def before_insert(self):
        branch = self.branch
        user_name = self.user_name
        doc_date = self.date
        current_date = datetime.today().date()
        date_difference = date_diff(current_date, doc_date)
        rec_count = self.get_the_record_count(branch, user_name, doc_date)
        # print(" ==+>", branch, user_name,  doc_date, current_date,
        #       date_difference, rec_count)
        if (self.is_new()):
            # print('is_new')
            if (rec_count == 0):
                # print(' rec_count == 0 ')
                if (date_difference < 0):
                    frappe.throw("You can't save the record with a future date")
                if (date_difference > 60):
                    frappe.throw("You cannot save a record that is over 60 days old")
                return
            elif (rec_count > 0):
                # print(' rec_count > 0 ')
                frappe.throw("You are limited to adding one record per day")

    def before_save(self):
        if (self.is_new()):
            return
        branch = self.branch
        user_name = self.user_name
        doc_date = self.date
        current_date = datetime.today().date()
        date_difference = date_diff(current_date, doc_date)
        rec_count = self.get_the_record_count(branch, user_name, doc_date)
        # print(" ==+>", branch, user_name,  doc_date, current_date,
        #       date_difference, rec_count)
        doc_date_changed = self.has_value_changed("date")
        # print('doc_date_changed ', doc_date_changed)
        if (doc_date_changed is False):
            if (date_difference > 60):
                frappe.throw("You cannot save a record that is over 60 days old")
            return
        # date is edited process
        if (rec_count > 0):
            frappe.throw("You are limited to adding one record per day")

        if (date_difference > 60):
            frappe.throw("You cannot save a record that is over 60 days old")

        if (date_difference < 0):
            frappe.throw("You shouldn't save the record with a future date")

    def get_the_record_count(self, branch, user_name, date_obj):
        rec_count = frappe.db.count(self.doctype, filters={
            'user_name': user_name,
            'branch': branch,
            'date': date_obj
        })
        return rec_count
