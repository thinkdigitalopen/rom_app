import frappe


@frappe.whitelist()
def delete_stock_related_data():
    frappe.db.delete("Inventory Summary")

    frappe.db.delete("Stock Entry Child")
    frappe.db.delete("Chef Indent By Dept Child")
    frappe.db.delete("Inventory Wastage Child")
    frappe.db.delete("Inventory Counting Child")

    frappe.db.delete("Stock Entry")
    frappe.db.delete("Chef Indent By Dept")
    frappe.db.delete("Inventory Wastage")
    frappe.db.delete("Inventory Counting")

    msg = """
    deleted successfully the following tables:

    Inventory Summary

    Stock Entry Child
    Stock Entry

    Chef Indent By Dept Child
    Chef Indent By Dept

    Inventory Wastage Child
    Inventory Wastage

    Inventory Counting Child
    Inventory Counting
    """
    return msg


@frappe.whitelist()
def reset_auto_increment():
    # sql = "ALTER TABLE `tabRaw Material Only` AUTO_INCREMENT = 1"
    sql = "TRUNCATE TABLE `tabRaw Material Only`"
    res = frappe.db.sql(sql)
    return res


