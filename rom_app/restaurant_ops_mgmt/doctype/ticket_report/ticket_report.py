import frappe
from frappe.model.document import Document
from datetime import datetime


class TicketReport(Document):
    def on_update(self):
        current_date = datetime.today().date()
        doc_save_date = datetime.strptime(self.date, '%Y-%m-%d').date()
        if (current_date > doc_save_date):
            frappe.throw("Editing records from the past is not permitted")
        # user_roles = frappe.get_roles(frappe.session.user)
        # # user_has_rm_role = user_roles.count('Rom_RM_Role')
        # user_has_chef_role = user_roles.count('Rom_Chef_Role')
        # print('============================')
        # print(user_roles)
        # print(user_has_chef_role)
        # print('self.completed')
        # print(self.completed)
        # print(type(self.completed))
        # if (user_has_chef_role >= 1):
        #     print('user_has_chef_role >= 1')
        #     if (self.completed == 1):
        #         print('self.completed == 1')
        #         frappe.throw("Editing completed record is not permitted")
