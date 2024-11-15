import frappe
from frappe.model.document import Document


class RawMaterialOnly(Document):
    def before_insert(self):
        # print('before_insert')
        rec_count = frappe.db.count(self.doctype, filters={
            'branch': self.branch,
            'item': self.item,
        })
        if (rec_count == 1):
            frappe.throw("This item is already available in this branch")

    def validate(self):
        # print('validate ==============================')
        rec_already_exist = frappe.db.count(self.doctype, filters={
            'name': self.name})
        if (rec_already_exist == 1):
            # print('update -=-=-=-=-=')
            db_doc = frappe.get_doc(self.doctype, self.name)
            # print('cur-db ', db_doc.name, db_doc.branch, db_doc.item,
                  #db_doc.unit, db_doc.price)
            # print('self   ', self.name, self.branch, self.item,
                  #self.unit, self.price)

            get_fields = ['name', 'branch',
                          'item', 'unit', 'price']

            result_list = frappe.db.get_list(self.doctype,
                                             filters={
                                                 'branch': self.branch,
                                                 'item': self.item},
                                             fields=get_fields, as_list=True)
            # print(result_list)
            list_count = len(result_list)
            # print('list_count', list_count)
            if (list_count == 1):
                list_rec = result_list[0]
                # print('list_rec', list_rec)
                list_rec_name = list_rec[0]
                # print('list_rec_name ', list_rec_name)
                if (list_rec_name != db_doc.name):
                    frappe.throw("This item is available in this branch")
