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
            'branch': d.branch,
            'item': d.item,
            'category_name': d.category_name,
            'group_name': d.group_name,
            'standard_stock': d.standard_stock,
            'price':  d.price,
            'attach_image':  d.attach_image,
        })
        data.append(row)

    data_with_anchor = formate_link_column_to_anchor_link(data)
    print('data_with_anchor')
    # print(data_with_anchor)
    return columns, data_with_anchor


def get_columns():
    return [
        {
            'fieldname': 'name',
            'label': 'Id',
            'fieldtype': 'Link',
            'options': 'Asset Master',
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
            'fieldname': 'category_name',
            'label': 'Category',
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
            'fieldname': 'price',
            'label': 'Price',
            'fieldtype': 'Currency',
        },
        {
            'fieldname': 'attach_image',
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
            asset.name,
            asset.branch,
            asset.item,
            cat.category_name,
            grp.group_name,
            asset.standard_stock,
            asset.price,
            asset.attach_image
        FROM
            `tabAsset Master` asset
        INNER JOIN
            `tabCategory` cat
        ON
            asset.category = cat.name
        LEFT JOIN
            `tabAsset Master Group` grp
        ON
            grp.name = asset.asset_group
        """
    where_cond = " WHERE 1 = 1 "
    if "branch_filter" in conditions:
        where_cond = where_cond + f" AND asset.branch = '{conditions['branch_filter']}' "
    if "category_filter" in conditions:
        where_cond = where_cond + f" AND cat.category_name LIKE '%{conditions['category_filter']}%' "
    if "item_filter" in conditions:
        where_cond = where_cond + f" AND asset.item LIKE '%{conditions['item_filter']}%' "
    if "group_filter" in conditions:
        where_cond = where_cond + f" AND grp.name = '{conditions['group_filter']}' "

    build_sql = f"{build_sql}  {where_cond}"
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


def formate_link_column_to_anchor_link(data):
    # /private/files/elephant.jpg
    domain_url = get_domain_name_of_the_site()
    for d in data:
        attach_image_url = d.attach_image
        formatted_url = formate_the_url(domain_url, attach_image_url)
        print(formatted_url)
        d.attach_image = formatted_url
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


