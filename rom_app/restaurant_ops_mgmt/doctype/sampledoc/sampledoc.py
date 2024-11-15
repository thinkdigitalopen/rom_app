import frappe
from frappe.model.document import Document


class SampleDoc(Document):
    def on_save(self):
        doc = frappe.get_doc(
            {
                'doctype': 'SampleDoc',
                'full_name': 'John',
            }
            )
        doc.insert()

