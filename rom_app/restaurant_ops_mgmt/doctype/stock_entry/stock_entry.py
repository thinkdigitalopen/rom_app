import frappe
from datetime import datetime
from frappe.model.document import Document
import rom_app.scheduled_tasks
from frappe.utils import now


class StockEntry(Document):
    # @frappe.whitelist()
    # def get_raw_material(self, branch, stock_entry_template):
    #     print("inside python")
    #     print("branch")
    #     print(branch)
    #     print("stock_entry_template")
    #     print(stock_entry_template)
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
    #     print(sql)
    #     item_data = frappe.db.sql(sql, as_dict=0)
    #     # # res_length = len(item_data)
    #     # # print(res_length)
    #     print(item_data)
    #     return item_data

    def validate(self):
        current_date = datetime.today().date()
        doc_save_date = datetime.strptime(self.date, '%Y-%m-%d').date()
        if (current_date > doc_save_date):
            frappe.throw("Editing records from the past is not permitted")

    def before_save(self):
        print('before save -=-=-=- ')
        print(self)
        for item in self.raw_material_from_template:
            print('items -=-=-=- >>> ')
            doc = frappe.get_doc('Raw Material Only', item.raw_material)
            print(" raw material - title ", doc.item)
            print(" raw material - price ", doc.price)
            print(" se - price  ", item.unit_price)
            doc.price = item.unit_price
            doc.save()

    def on_update(self):
        print(' >> on_update << ')
        print(self)
        print("Formatted date and time:", now())
        frappe.enqueue(rom_app.scheduled_tasks.inventory_summary, queue='long')

    @frappe.whitelist()
    def get_raw_material_with_id(self, branch, template):
        print("inside python")
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
        print(sql)
        item_data = frappe.db.sql(sql, as_dict=0)
        res_length = len(item_data)
        print(res_length)
        print(item_data)
        return item_data
