import frappe
import yaml
import json


def execute(filters=None):
    print("=========================")
    print(yaml.dump(filters))
    data, columns = [], []
    columns = get_columns()
    cs_data = get_data(filters)
    data = []
    for d in cs_data:
        row = frappe._dict({
            'name': d.name,
            'date': d.date,
            'branch': d.branch,
            'item': d.item,
            'unit': d.unit,
            'price': d.price,
            'closing_stock': d.closing_stock,
            'closing_amount': d.closing_amount,
            'min_stock': d.min_stock,
            'group_name': d.group_name
        })
        data.append(row)

    return columns, data


def get_columns():
    return [
        {
            'fieldname': 'name',
            'label': 'Id',
            'fieldtype': 'Link',
            'options': 'Raw Material Only',
        },
        {
            'fieldname': 'date',
            'label': 'Date',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'branch',
            'label': 'Branch',
            "fieldtype": "Data",
        },
        {
            'fieldname': 'item',
            'label': 'Item',
            'fieldtype': 'Data',
            'width': 350
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
            'fieldname': 'closing_stock',
            'label': 'Close. Stock',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'closing_amount',
            'label': 'Close. Amount',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'min_stock',
            'label': 'Min Stock',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'group_name',
            'label': 'RM Group',
            'fieldtype': 'Data',
        }
    ]


def get_data(filters):
    conditions = get_conditions(filters)
    print("-------- get data ------------")
    print(conditions)
    sql = build_sql(conditions)
    print("-------- full sql ------------")
    print(sql)
    data = frappe.db.sql(sql, as_dict=True)
    return data


def build_sql(conditions):
    sql = """
    SELECT
        raw.name,  raw.branch,  raw.item, raw.unit, raw.price,
        raw.closing_stock,raw.closing_amount,
        raw.min_stock, raw.`date`, rawgrp.group_name
    FROM
        `tabRaw Material Only` raw
    LEFT JOIN
        `tabRaw Material Group` rawgrp
     ON
       raw.rm_group = rawgrp.name
    """
    full_sql = get_where_filter(sql, conditions)
    return full_sql


def get_where_filter(sql, conditions):
    where_cond = " WHERE  1=1 "
    if "branch_filter" in conditions:
        where_cond = where_cond + f" AND raw.branch = '{conditions['branch_filter']}' "
    if "raw_material_filter" in conditions:
        where_cond = where_cond + f" AND raw.item  LIKE '%{conditions['raw_material_filter']}%'  "
    if "group_name_filter" in conditions:
        where_cond = where_cond + f" AND raw.rm_group = '{conditions['group_name_filter']}' "
    sql = f"{sql}  {where_cond}"
    return sql


def get_conditions(filters):
    conditions = {}
    if (type(filters) is str):
        filters = json.loads(filters)

    for key, value in filters.items():
        if filters.get(key):
            conditions[key] = value
    return conditions
