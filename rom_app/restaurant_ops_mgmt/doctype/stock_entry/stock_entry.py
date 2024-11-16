import frappe
from datetime import datetime
from frappe.model.document import Document
import rom_app.scheduled_tasks
from frappe.utils import now
from frappe.utils import date_diff
from ... import utils


class StockEntry(Document):
    # @frappe.whitelist()
    # def get_raw_material(self, branch, stock_entry_template):
    #     # print("inside python")
    #     # print("branch")
    #     # print(branch)
    #     # print("stock_entry_template")
    #     # print(stock_entry_template)
    #     sql = """
    #     SELECT chi.raw_material, chi.unit, raw.price, raw.item, raw.closing_stock
    #     FROM `tabStock Entry Template` par
    #     INNER JOIN `tabStock Entry Template Child` chi
    #     ON par.name = chi.parent
    #     INNER JOIN `tabRaw Material Only` raw
    #     ON raw.name = chi.raw_material
    #     WHERE par.branch = '{}' AND par.stock_entry_template = '{}'
    #     """
    #     sql = sql.format(branch, stock_entry_template)
    #     # print(sql)
    #     item_data = frappe.db.sql(sql, as_dict=0)
    #     # # res_length = len(item_data)
    #     # # # print(res_length)
    #     # print(item_data)
    #     return item_data

    def validate(self):
        doc_date = self.date
        current_date = datetime.today().date()
        date_difference = date_diff(current_date, doc_date)
        # print('date_difference ', date_difference)
        if (date_difference > 60):
            frappe.throw("You cannot save a record that is over 60 days old")

    def before_save(self):
        # # print('before save -=-=-=- ')
        # print(self)
        for item in self.raw_material_from_template:
            # # print('items -=-=-=- >>> ')
            doc = frappe.get_doc('Raw Material Only', item.raw_material)
            # # print(" raw material - title ", doc.item)
            # # print(" raw material - price ", doc.price)
            # # print(" se - price  ", item.unit_price)
            doc.price = item.unit_price
            doc.save()

    def on_update(self):
        print(' >> on_update << ')
        # print(self)
        # # print("Formatted date and time:", now())
        user_email = frappe.session.user
        branch = utils.find_user_branch_based_on_email(user_email)
        doc_date = self.date
        # doc_date = doc_date.strftime("%Y-%m-%d")
        print("on_update - branch: docdate", branch, doc_date)
        # rom_app.scheduled_tasks.inventory_summary(branch, doc_date)
        frappe.enqueue(
            rom_app.scheduled_tasks.inventory_summary,
            queue='long',
            p_branch=branch, p_date=doc_date)

    def after_delete(self):
        user_email = frappe.session.user
        branch = utils.find_user_branch_based_on_email(user_email)
        # print("on_update - branch:", branch)
        doc_date = self.date
        doc_date = doc_date.strftime("%Y-%m-%d")
        print("on_update - branch: docdate", branch, doc_date)
        print(' >> after_delete << <<<<<<<<<<<<<<<<<<< ')
        # rom_app.scheduled_tasks.inventory_summary(branch, doc_date)
        frappe.enqueue(
            rom_app.scheduled_tasks.inventory_summary,
            queue='long',
            p_branch=branch, p_date=doc_date)

    @frappe.whitelist()
    def get_raw_material_with_id(self, branch, template):
        # print("inside python")
        sql = """
        SELECT
            rawmat.item,
            child.unit,
            rawmat.price,
            rawmat.name
        FROM
           `tabStock Entry Template` parent
        JOIN
           `tabStock Entry Template Child` child
        ON
            parent.name = child.parent
        JOIN
            `tabRaw Material Only` rawmat
        ON
            rawmat.name = child.raw_material
        WHERE
            parent.branch = '{}'
        AND
            parent.stock_entry_template = '{}'
        ORDER BY child.idx ASC
        """
        sql = sql.format(branch, template)
        # # print(sql)
        item_data = frappe.db.sql(sql, as_dict=0)
        # res_length = len(item_data)
        # # print(res_length)
        # # print(item_data)
        return item_data
