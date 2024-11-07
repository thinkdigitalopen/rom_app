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
            'branch': d.branch,
            'menu_item': d.menu_item,
            'menu_group_name': d.menu_group_name,
            'unit': d.unit,
            'price': d.price,
        })
        data.append(row)

    return columns, data


def get_columns():
    return [
        {
            'fieldname': 'name',
            'label': 'Id',
            'fieldtype': 'Link',
            'options': 'Menu',
        },
        {
            'fieldname': 'branch',
            'label': 'Branch',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'menu_item',
            'label': 'Menu Item',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'menu_group_name',
            'label': 'Group',
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
        }
    ]


def get_data(filters):
    conditions = get_conditions(filters)
    print("-------- get data ------------")
    print(conditions)
    build_sql = """
        SELECT tm.name, tm.branch, tm.menu_item,
        grp.menu_group_name, tm.unit, tm.price
        FROM
        `tabMenu` tm
        LEFT JOIN
       `tabMenu Group` grp
        ON
        tm.group_name = grp.name
        """
    where_cond = " WHERE 1 =1  "
    if "branch_filter" in conditions:
        where_cond = where_cond + f" AND tm.branch = '{conditions['branch_filter']}' "
    if "menu_group_filter" in conditions:
        where_cond = where_cond + f" AND tm.group_name = '{conditions['menu_group_filter']}' "
    if "menu_item_filter" in conditions:
        where_cond = where_cond + f" AND tm.menu_item LIKE '%{conditions['menu_item_filter']}%' "
    build_sql = f"{build_sql}  {where_cond}"
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
