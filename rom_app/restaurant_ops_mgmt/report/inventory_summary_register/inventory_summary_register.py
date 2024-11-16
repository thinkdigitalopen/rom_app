import frappe
import yaml
import json


def execute(filters=None):
    # print("=========================")
    # print(yaml.dump(filters))
    data, columns = [], []
    columns = get_columns()
    cs_data = get_data(filters)
    # branch date raw_material quantity price unit closing_quantity
    data = []
    for d in cs_data:
        row = frappe._dict({
            'name': d.name,
            'date': d.date,
            'branch': d.branch,
            'raw_material': d.raw_material,
            'rm_group': d.rm_group,
            'quantity': d.quantity,
            'unit': d.unit,
            'price': d.price,
            'closing_quantity': d.closing_quantity,
            'closing_amount': d.closing_amount,
            'min_stock': d.min_stock,
            'cs_ms': d.cs_ms
        })
        data.append(row)

    return columns, data


def get_columns():
    return [
        {
            'fieldname': 'name',
            'label': 'Id',
            'fieldtype': 'Link',
            'options': 'Inventory Summary',
        },
        {
            'fieldname': 'date',
            'label': 'Date',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'branch',
            'label': 'Branch',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'raw_material',
            'label': 'Raw Material',
            'fieldtype': 'Data',
            'width': 300
        },
        {
            'fieldname': 'rm_group',
            'label': 'RM Group',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'quantity',
            'label': 'Current Qty',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'unit',
            'label': 'Unit',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'price',
            'label': 'Price',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'closing_quantity',
            'label': 'Closing Stock',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'closing_amount',
            'label': 'Closing Amount',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'min_stock',
            'label': 'Min Stock',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'cs_ms',
            'label': 'Clos.St - Min',
            'fieldtype': 'Data',
        }
    ]


def get_data(filters):
    conditions = get_conditions(filters)
    # print("-------- get data ------------")
    # print(conditions)
    build_sql = """
    SELECT
    inv.name,
    inv.date,
    raw.item as raw_material,
    rmgrp.group_name  as rm_group,
    inv.branch,
    inv.quantity,
    inv.price,
    inv.unit,
    inv.closing_quantity,
    inv.closing_amount,
    raw.min_stock,
    (inv.closing_quantity - raw.min_stock) as cs_ms
    FROM `tabInventory Summary` inv
    INNER JOIN `tabRaw Material Only` raw ON inv.raw_material = raw.name
    LEFT JOIN `tabRaw Material Group` rmgrp ON raw.rm_group = rmgrp.name
        """
    # INNER JOIN `tabBranch` bra ON inv.branch = bra.name
    where_cond = f" WHERE inv.date between '{conditions['from_date_filter']}' AND '{conditions['to_date_filter']}' "

    if "branch_filter" in conditions:
        where_cond = where_cond + f" AND inv.branch = '{conditions['branch_filter']}' "
    if "raw_material_filter" in conditions:
        where_cond = where_cond + f" AND inv.raw_material = '{conditions['raw_material_filter']}' "
    if "rmgroup_filter" in conditions:
        where_cond = where_cond + f" AND raw.rm_group = '{conditions['rmgroup_filter']}' "

    build_sql = f"{build_sql}  {where_cond}"
    # print("-------- full sql ------------")
    # print(build_sql)
    data = frappe.db.sql(build_sql, as_dict=True)
    return data


def get_conditions(filters):
    conditions = {}
    if (type(filters) is str):
        filters = json.loads(filters)

    for key, value in filters.items():
        if filters.get(key):
            conditions[key] = value

    return conditions
