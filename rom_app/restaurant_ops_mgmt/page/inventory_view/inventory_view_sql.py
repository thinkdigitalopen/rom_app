import frappe
import yaml
import json


@frappe.whitelist()
def inventory_valuation(filters):
    print("inv_value")
    conditions = get_conditions(filters)
    print("-------- get data ------------")
    print(conditions)
    sql = " select tis.`date`, sum(closing_amount) as inventory_valuation from `tabInventory Summary` tis"
    sql_where = build_sql_where_condition(sql, conditions)
    group_by = " GROUP By date "
    build_sql = f"{sql_where}  {group_by} "
    print(build_sql)
    data = execute_sql(build_sql)
    return data


@frappe.whitelist()
def inventory_wastage(filters):
    print("inventory_wastage")
    conditions = get_conditions(filters)
    print("-------- get data ------------")
    print(conditions)
    sql = " select tiw.`date`, tiw.total_price as inv_wastage from `tabInventory Wastage` tiw "
    sql_where = build_sql_where_condition(sql, conditions)
    group_by = " GROUP By date "
    build_sql = f"{sql_where}  {group_by} "
    print(build_sql)
    data = execute_sql(build_sql)
    return data


@frappe.whitelist()
def inventory_po(filters):
    print("inventory_po")
    conditions = get_conditions(filters)
    print("-------- get data ------------")
    print(conditions)
    sql = " select tpo.`date`, tpo.total_price as inv_po from `tabPurchase Order` tpo "
    sql_where = build_sql_where_condition(sql, conditions)
    group_by = " GROUP By date "
    build_sql = f"{sql_where}  {group_by} "
    print(build_sql)
    data = execute_sql(build_sql)
    return data


@frappe.whitelist()
def inventory_transaction_by_amount_data(filters):
    print("inventory_transaction_by_amount_data")
    conditions = get_conditions(filters)
    print("-------- get data ------------")
    print(conditions)
    sql_purchase_order = "SELECT 'Purchase Order' AS 'inventory_transaction', SUM(purchase_order.total_price) as 'total_amount' FROM `tabPurchase Order` purchase_order"
    sql_chef_indent = "SELECT 'Chef Indent' AS 'inventory_transaction', SUM(chef_indent.total_price) as 'total_amount' FROM `tabChef Indent By Dept` chef_indent"
    sql_invent_wastage = "SELECT 'Inventory Wastage' AS 'inventory_transaction', SUM(invent_wastage.total_price) as 'total_amount' FROM `tabInventory Wastage` invent_wastage"
    sql_invent_counting = "SELECT  'Inventory Counting' AS 'inventory_transaction',SUM(invent_counting.total_amount) as 'total_amount' FROM `tabInventory Counting` invent_counting"

    sql_purchase_order = build_sql_where_condition(sql_purchase_order, conditions)
    sql_chef_indent = build_sql_where_condition(sql_chef_indent, conditions)
    sql_invent_wastage = build_sql_where_condition(sql_invent_wastage, conditions)
    sql_invent_counting = build_sql_where_condition(sql_invent_counting, conditions)

    build_sql1 = f"  {sql_purchase_order} UNION  {sql_chef_indent} "
    build_sql2 = f" UNION  {sql_invent_wastage} UNION {sql_invent_counting} "

    build_sql = build_sql1 + build_sql2
    print(build_sql)
    data = execute_sql(build_sql)
    return data


@frappe.whitelist()
def top_ten_items_below_min_stock_data(filters):
    print("top_ten_items_below_min_stock_data")
    conditions = get_conditions(filters)
    print("-------- get data ------------")
    print(conditions)
    sql = """
    SELECT raw.item as raw_material, raw.min_stock, raw.closing_stock,
    ABS( (raw.closing_stock - raw.min_stock) ) AS min_difference
    FROM `tabRaw Material Only` raw
    WHERE raw.closing_stock < raw.min_stock
    ORDER BY min_difference DESC
    """
    full_sql = build_sql_where_condition(sql, conditions)
    print(full_sql)
    data = execute_sql(sql)
    return data


def build_sql_where_condition(build_sql, conditions):
    where_cond = f" WHERE date between '{conditions['from_date_filter']}' AND '{conditions['to_date_filter']}' "
    if "branch_filter" in conditions:
        where_cond = where_cond + f" AND branch_id = '{conditions['branch_filter']}' "
    build_sql = f"{build_sql}  {where_cond}"
    return build_sql


def execute_sql(build_sql):
    print("-------- full sql ------------")
    print(build_sql)
    data = frappe.db.sql(build_sql, as_dict=True)
    print(data)
    return data


def get_conditions(filters):
    conditions = {}
    if (type(filters) is str):
        filters = json.loads(filters)

    for key, value in filters.items():
        if filters.get(key):
            conditions[key] = value
    return conditions
