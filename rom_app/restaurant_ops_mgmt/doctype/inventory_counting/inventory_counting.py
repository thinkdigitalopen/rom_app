import frappe
from frappe.model.document import Document
from datetime import datetime
import rom_app.scheduled_tasks
from frappe.utils import now
from ... import utils


class InventoryCounting(Document):
    def before_insert(self):
        current_date = datetime.today().date()
        doc_save_date = datetime.strptime(self.date, '%Y-%m-%d').date()
        if (current_date > doc_save_date):
            frappe.throw("Editing records from the past is not permitted")

    def on_update(self):
        print(' >> on_update << ')
        print(self)
        print("Formatted date and time:", now())
        user_email = frappe.session.user
        branch = utils.find_user_branch_based_on_email(user_email)
        print("on_update - branch:", branch)
        # rom_app.scheduled_tasks.inventory_summary(branch)
        frappe.enqueue(
            rom_app.scheduled_tasks.inventory_summary,
            queue='long',
            param_branch=branch)
