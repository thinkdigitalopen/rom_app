import frappe
from datetime import datetime
from frappe.model.document import Document


class AssetCount(Document):
    pass
    # def before_insert(self):
    #     branch = self.branch
    #     user_name = self.user_name
    #     current_date = datetime.today().date()
    #     category_name = ''
    #     roles = frappe.get_roles(frappe.session.user)
    #     print(roles)
    #     if "Rom_DM_Role" in roles:
    #         category_name = 'Dining'
    #     if "Rom_Chef_Role" in roles:
    #         category_name = 'Kitchen'
    #     print('-------------------------------------------')
    #     print(f" {branch} {user_name} {current_date} {category_name} " )
    #     rec_count = self.get_the_record_count(branch, user_name, current_date)
    #     print(f" rec_count {rec_count}  ")
    #     if (rec_count > 0):
    #         frappe.throw("You are limited to adding just one record per day.")

    # def validate(self):
    #     current_date = datetime.today().date()
    #     doc_save_date = datetime.strptime(self.date, '%Y-%m-%d').date()
    #     if (current_date > doc_save_date):
    #         frappe.throw("Editing records from the past is not permitted")

    # def get_the_record_count(self, branch, user_name, date_obj, category_name):
    #     rec_count = frappe.db.count('Asset Count', filters={
    #         'user_name': user_name,
    #         'branch': branch,
    #         'date': date_obj
    #     })
    #     return rec_count
