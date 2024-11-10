import frappe
import yaml
import json
import socket


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
            'user_name': d.user_name,
            'branch': d.branch,
            'item': d.item,
            'group_name': d.group_name,
            'standard_stock': d.standard_stock,
            'current_stock': d.current_stock,
            'difference':  d.difference,
            'diff_filled':  d.diff_filled,
            'asset_master_image':  d.asset_master_image
        })
        data.append(row)

    data_with_anchor = formate_link_column_to_anchor_link(data)
    print('data_with_anchor')

    return columns, data_with_anchor


def get_columns():
    return [
        {
            'fieldname': 'name',
            'label': 'Id',
            'fieldtype': 'Link',
            'options': 'Asset Count',
        },
        {
            'fieldname': 'date',
            'label': 'Date',
            'fieldtype': 'Date',
        },
        {
            'fieldname': 'user_name',
            'label': 'User Name',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'branch',
            'label': 'Branch',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'item',
            'label': 'Item',
            'fieldtype': 'Data',
            'width': '160',
        },
        {
            'fieldname': 'group_name',
            'label': 'Group',
            'fieldtype': 'Data',
            'width': '160',
        },
        {
            'fieldname': 'standard_stock',
            'label': 'Std. Stock',
            'fieldtype': 'Int',
        },
        {
            'fieldname': 'current_stock',
            'label': 'Curr. Stock',
            'fieldtype': 'Int',
        },
        {
            'fieldname': 'difference',
            'label': 'Difference',
            'fieldtype': 'Int',
        },
        {
            'fieldname': 'diff_filled',
            'label': 'Diff Filled',
            'fieldtype': 'Check',
        },
        {
            'fieldname': 'asset_master_image',
            'label': 'Image',
            'fieldtype': 'Image',
        }
    ]


def get_data(filters):
    conditions = get_conditions(filters)
    print("-------- get data ------------")
    print(conditions)
    build_sql = """
    SELECT
    ic.name,
    ic.date,
    ic.user_name,
    ic.branch,
    icc.item,
    icc.group_name,
    icc.standard_stock,
    icc.current_stock,
    icc.difference,
    icc.diff_filled,
    icc.asset_master_image
    FROM
    `tabAsset Count` ic
    INNER JOIN
    `tabAsset Count Child` icc
    ON ic.name = icc.parent
        """
    where_cond = f" WHERE ic.`date` between '{conditions['from_date_filter']}' AND  '{conditions['to_date_filter']}' "
    if "branch_filter" in conditions:
        where_cond = where_cond + f" AND ic.branch = '{conditions['branch_filter']}' "
    if "category_filter" in conditions:
        where_cond = where_cond + f" AND ic.category_id = '{conditions['category_filter']}' "
    if "item_filter" in conditions:
        where_cond = where_cond + f" AND icc.item LIKE '%{conditions['item_filter']}%' "
    if "group_filter" in conditions:
        where_cond = where_cond + f" AND icc.asset_group_id = '{conditions['group_filter']}' "
    if "diff_filled_filter" in conditions:
        where_cond = where_cond + f" AND icc.diff_filled = '{conditions['diff_filled_filter']}' "

    order_by = " ORDER BY ic.date DESC, icc.idx ASC "

    build_sql = f"{build_sql}  {where_cond} {order_by}"
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


@frappe.whitelist()
def get_data_by_difference(filters):
    conditions = get_conditions(filters)
    print("--------  get_data_by_difference ------------")
    print(conditions)
    build_sql = """
    SELECT
    ic.date,
    sum(icc.difference) as difference
    FROM
    `tabAsset Count` ic
    INNER JOIN
    `tabAsset Count Child` icc
    ON ic.name = icc.parent
        """
    where_cond = f" WHERE ic.`date` between '{conditions['from_date_filter']}' AND  '{conditions['to_date_filter']}' "
    if "branch_filter" in conditions:
        where_cond = where_cond + f" AND ic.branch = '{conditions['branch_filter']}' "

    group_by = " GROUP By ic.date "
    order_by = " ORDER BY ic.date DESC "

    build_sql = f"{build_sql}  {where_cond} {group_by} {order_by}"
    print("-------- full sql ------------")
    print(build_sql)
    data = frappe.db.sql(build_sql, as_dict=True)
    return data


def formate_link_column_to_anchor_link(data):
    # /private/files/elephant.jpg
    domain_url = get_domain_name_of_the_site()
    for d in data:
        attach_image_url = d.asset_master_image
        formatted_url = formate_the_url(domain_url, attach_image_url)
        print(formatted_url)
        d.asset_master_image = formatted_url
    return data


def formate_the_url(domain_name, attach_image_url):
    farmate_part_url = f"{domain_name}{attach_image_url}"
    if (attach_image_url is None):
        farmate_part_url = ''

    anchor = f"<img src='{farmate_part_url}' style='width: 120px; height: 120px;'></img>"
    return anchor


def get_domain_name_of_the_site():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    print("Your Computer Name is:" + hostname)
    print("Your Computer IP Address is:" + IPAddr)
    domain_url = frappe.db.get_value('Rom Settings',
                                     {'settings_name': 'domain_name'},
                                     ['settings_value'])
    print('domain_url ---> ', domain_url)
    return domain_url
