import frappe


@frappe.whitelist()
def delete_stock_related_data():
    frappe.db.delete("Inventory Summary")
    frappe.db.delete("Stock Entry")
    frappe.db.delete("Chef Indent By Dept")
    frappe.db.delete("Inventory Wastage")
    frappe.db.delete("Inventory Counting")
    return "deleted successfully"


