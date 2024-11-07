import frappe
import yaml
import json


def execute(filters=None):
    print("=========================")
    print(yaml.dump(filters))
    data, columns = [], []
    columns = get_columns()
    cs_data = get_data(filters)
    # branch  date  user_name   branch
    # raw_material unit quantity price clos_stock remarks
    data = []
    for d in cs_data:
        row = frappe._dict({
            'name': d.name,
            'date': d.date,
            'branch': d.branch,
            'user_name': d.user_name,
            'raw_material': d.raw_material,
            'unit': d.unit,
            'quantity': d.quantity,
            'price': d.price,
            'clos_stock': d.clos_stock
        })
        data.append(row)

    print(data)
    return columns, data


def get_columns():
    return [
        {
            'fieldname': 'name',
            'label': 'Id',
            'fieldtype': 'Link',
            'options': 'Inventory Counting',
        },
        {
            'fieldname': 'date',
            'label': 'Date',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'branch',
            'label': 'Branch Name',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'user_name',
            'label': 'User Name',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'raw_material',
            'label': 'Raw Material',
            'fieldtype': 'Data',
            'width': 400
        },
        {
            'fieldname': 'unit',
            'label': 'Unit',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'quantity',
            'label': 'Count Qty',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'price',
            'label': 'Price',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'clos_stock',
            'label': 'Close Stock',
            'fieldtype': 'Data',
        }
    ]


def get_data(filters):
    conditions = get_conditions(filters)
    print("-------- get data ------------")
    print(conditions)
    build_sql = """
    SELECT
        par.name,
        par.branch,
        par.date,
        par.user_name,
        raw.item as raw_material,
        chi.unit,
        chi.quantity as quantity,
        chi.price,
        chi.clos_stock
    FROM
        `tabInventory Counting`  par
    INNER JOIN `tabInventory Counting Child` chi ON
        chi.parent = par.name
    INNER JOIN `tabRaw Material Only` raw ON
        chi.raw_material = raw.name
    """
    where_cond = f" WHERE par.date between '{conditions['from_date_filter']}' AND '{conditions['to_date_filter']}' "

    if "branch_filter" in conditions:
        where_cond = where_cond + f" AND par.branch = '{conditions['branch_filter']}' "
    if "raw_material_filter" in conditions:
        where_cond = where_cond + f" AND raw_material = '{conditions['raw_material_filter']}' "

    order_by = "ORDER BY name DESC"
    build_sql = f"{build_sql}  {where_cond}  {order_by}"
    print("-------- full sql ------------")
    print(build_sql)
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
