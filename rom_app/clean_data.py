import frappe


@frappe.whitelist()
def delete_stock_related_data():
    frappe.db.delete("Inventory Summary")
    #
    frappe.db.delete("Stock Entry Child")
    frappe.db.delete("Chef Indent By Dept Child")
    frappe.db.delete("Inventory Wastage Child")
    # frappe.db.delete("Inventory Counting Child")
    #
    frappe.db.delete("Stock Entry")
    frappe.db.delete("Chef Indent By Dept")
    frappe.db.delete("Inventory Wastage")
    # frappe.db.delete("Inventory Counting")
    sql = "Update `tabRaw Material Only` SET closing_stock = 0, closing_amount = 0"
    frappe.db.sql(sql, as_dict=True)
    msg = """
    deleted successfully the following tables:
    Inventory Summary
    Raw material Closing data set to zero
    Stock Entry Child
    Stock Entry
    Chef Indent By Dept Child
    Chef Indent By Dept
    Inventory Wastage Child
    Inventory Wastage
    """
    return msg


@frappe.whitelist()
def reset_auto_increment():
    # sql = "ALTER TABLE `tabRaw Material Only` AUTO_INCREMENT = 1"
    sql = "TRUNCATE TABLE `tabRaw Material Only`"
    res = frappe.db.sql(sql)
    return res


