import frappe
from datetime import datetime
from frappe.model.document import Document


class StockEntry(Document):
    @frappe.whitelist()
    def get_raw_material(self, branch, stock_entry_template):
        print("inside python")
        print("branch")
        print(branch)
        print("stock_entry_template")
        print(stock_entry_template)
        sql = """
        SELECT chi.raw_material, chi.unit, chi.price, raw.item, raw.closing_stock
        FROM `tabStock Entry Template` par
        INNER JOIN `tabStock Entry Template Child` chi
        ON par.name = chi.parent
        INNER JOIN `tabRaw Material Only` raw
        ON raw.name = chi.raw_material
        WHERE par.branch = '{}' AND par.stock_entry_template = {}
        """
        sql = sql.format(branch, stock_entry_template)
        print(sql)
        item_data = frappe.db.sql(sql, as_dict=0)
        # # res_length = len(item_data)
        # # print(res_length)
        print(item_data)
        return item_data

    def on_update(self):
        current_date = datetime.today().date()
        doc_save_date = datetime.strptime(self.date, '%Y-%m-%d').date()
        if (current_date > doc_save_date):
            frappe.throw("Editing records from the past is not permitted")
