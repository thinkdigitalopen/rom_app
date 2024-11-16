import frappe
from frappe.model.document import Document
from datetime import datetime
import rom_app.scheduled_tasks
from frappe.utils import date_diff
from frappe.utils import now
from ... import utils


class InventoryWastage(Document):
    def validate(self):
        doc_date = self.date
        current_date = datetime.today().date()
        date_difference = date_diff(current_date, doc_date)
        print('date_difference ', date_difference)
        if (date_difference > 60):
            frappe.throw("You cannot save a record that is over 60 days old")

    def on_update(self):
        print(' >> on_update << ')
        print(self)
        print("Formatted date and time:", now())
        user_email = frappe.session.user
        branch = utils.find_user_branch_based_on_email(user_email)
        print("on_update - branch:", branch)
        doc_date = self.date
        # rom_app.scheduled_tasks.inventory_summary(branch, doc_date)
        frappe.enqueue(
            rom_app.scheduled_tasks.inventory_summary,
            queue='long',
            param_branch=branch, param_date=doc_date)

    def after_delete(self):
        user_email = frappe.session.user
        branch = utils.find_user_branch_based_on_email(user_email)
        # print("on_update - branch:", branch)
        doc_date = self.date
        doc_date = doc_date.strftime("%Y-%m-%d")
        print("after_delete - branch: docdate", branch, doc_date)
        print(' >> after_delete << <<<<<<<<<<<<<<<<<<< ')
        # rom_app.scheduled_tasks.inventory_summary(branch, doc_date)
        frappe.enqueue(
            rom_app.scheduled_tasks.inventory_summary,
            queue='long',
            p_branch=branch, p_date=doc_date)
