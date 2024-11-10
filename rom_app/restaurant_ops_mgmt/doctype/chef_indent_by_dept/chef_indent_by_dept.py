import frappe
from frappe.model.document import Document
from datetime import datetime
import rom_app.scheduled_tasks
from frappe.utils import now
from frappe.utils import date_diff


class ChefIndentByDept(Document):
    def validate(self):
        doc_date = self.date
        current_date = datetime.today().date()
        date_difference = date_diff(current_date, doc_date)
        print('date_difference ', date_difference)
        if (date_difference > 0):
            frappe.throw("You cannot save the record with a past date")

    def before_save(self):
        print('before save python')
        print('^^^^^^^^^^^^^^^^^^^')
        print(self)
        print('^^^^^^^^^^^^^^^^^^^')
        print(self.raw_materials)
        for item in self.raw_materials:
            print('------------------------------ - ')
            if (item.issu_qty_entry is None):
                return
            print('item.issu_qty_entry - ', item.issu_qty_entry)
            # print('item.issued_qty - ', item.issued_qty)
            if (item.issu_qty_entry == 0):
                print('==0')
                issu_qty_entry_minus = 0
            else:
                print('!=0')
                issu_qty_entry_minus = -1 * item.issu_qty_entry
            print('issu_qty_entry_minus ', issu_qty_entry_minus)
            item.issued_qty = issu_qty_entry_minus
            print('item.issued_qty ', item.issued_qty)

    def get_the_record_count(self, branch, user_name, date_obj):
        rec_count = frappe.db.count('Chef Indent By Dept', filters={
            'user_name': user_name,
            'branch': branch,
            'date': date_obj
        })
        return rec_count

    def listToString(s):
        str1 = " "
        return (str1.join(s))

    @frappe.whitelist()
    def get_raw_material(self, branch, department):
        print("inside python")
        sql = """
        SELECT rawmat.item, child.indent_unit, rawmat.name
        FROM `tabRaw Material For Indent` parent
        JOIN `tabRaw Material For Indent Child` child
        ON	parent.name = child.parent
        JOIN `tabRaw Material Only` rawmat
        ON	rawmat.name = child.raw_material
        WHERE parent.branch = '{}'
        AND parent.department = '{}';
        """
        sql = sql.format(branch, department)
        print(sql)
        item_data = frappe.db.sql(sql, as_dict=0)
        res_length = len(item_data)
        print(res_length)
        print(item_data)
        return item_data

    @frappe.whitelist()
    def get_raw_material_with_id(self, branch, department):
        print("inside python")
        sql = """
        SELECT child.raw_material, child.indent_unit, trmo.item,
        trmo.price, trmo.closing_stock
        FROM `tabRaw Material For Indent` parent
        JOIN `tabRaw Material For Indent Child` child
        ON	parent.name = child.parent
        JOIN `tabRaw Material Only` trmo
        ON child.raw_material  = trmo.name
        WHERE parent.branch = '{}'
        AND parent.department = '{}';
        """
        sql = sql.format(branch, department)
        print(sql)
        item_data = frappe.db.sql(sql, as_dict=0)
        res_length = len(item_data)
        print(res_length)
        print(item_data)
        return item_data

    # @frappe.whitelist()
    # def test(self):
    #     print('item_data')
    #     return 'item_data'



    def on_update(self):
        print(' >> on_update << ')
        print(self)
        print("Formatted date and time:", now())
        frappe.enqueue(rom_app.scheduled_tasks.inventory_summary, queue='long')

        # user_roles = frappe.get_roles(frappe.session.user)
        # # user_has_rm_role = user_roles.count('Rom_RM_Role')
        # user_has_chef_role = user_roles.count('Rom_Chef_Role')
        # print('============================')
        # print(user_roles)
        # print(user_has_chef_role)
        # print('self.rm_approval')
        # print(self.rm_approval)
        # print(type(self.rm_approval))
        # if (user_has_chef_role >= 1):
        #     print('user_has_chef_role >= 1')
        #     if (self.rm_approval == 1):
        #         print('self.rm_approval == 1')
        #         frappe.throw("Editing approved record is not permitted")

    #     # find the document branch name
    #     doc_branch = self.branch
    #     print('doc_branch', doc_branch)
    #     # find current user branch name
    #     user_branch = self.find_user_branch()
    #     print('user_branch', user_branch)
    #     if (doc_branch != user_branch):
    #         frappe.throw("Editing other branch record is not permitted")
    #
    # def find_user_branch(self):
    #     user_email = frappe.session.user
    #     sql = """
    #     select userbranch.branch from `tabUser to Branch Assignment` userbranch
    #     WHERE
    #     userbranch.user = '{}';
    #     """
    #     sql = sql.format(user_email)
    #     print(sql)
    #     item_data = frappe.db.sql(sql, as_dict=0)
    #     res_length = len(item_data)
    #     print(res_length)
    #     print(item_data)
    #     return item_data[0][0]
