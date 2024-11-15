import frappe
import yaml
import json


def execute(filters=None):
    print("=========================")
    print(yaml.dump(filters))
    data, columns = [], []
    columns = get_columns()
    cs_data = get_data(filters)
    #  date  branch  user_name  branch
    # raw_material  unit  ord_qty  price  total_price  clos_qty
    data = []
    for d in cs_data:
        row = frappe._dict({
            'name': d.name,
            'date': d.date,
            'branch': d.branch,
            'user_name': d.user_name,
            'template_type_name': d.template_type_name,
            'raw_material': d.raw_material,
            'unit': d.unit,
            'ord_qty': d.ord_qty,
            'price': d.price,
            'total_price': d.total_price,
            'bill_date': d.bill_date,
            'ref_no': d.ref_no,
            'remarks': d.remarks
        })
        data.append(row)

    return columns, data


def get_columns():
    return [
        {
            'fieldname': 'name',
            'label': 'Id',
            'fieldtype': 'Link',
            'options': 'Stock Entry',
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
            'fieldname': 'template_type_name',
            'label': 'Vendor',
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
            'fieldname': 'ord_qty',
            'label': 'Order Qty',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'price',
            'label': 'Price',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'total_price',
            'label': 'Total Price',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'bill_date',
            'label': 'Bill Date',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'ref_no',
            'label': 'Ref No',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'remarks',
            'label': 'Remarks',
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
        tv.template_type_name,
        raw.item as raw_material,
        chi.unit,
        chi.ord_qty,
        chi.unit_price as price,
        chi.amount as total_price,
        par.bill_date,
        par.ref_no,
        par.remarks
    FROM
        `tabStock Entry` par
    LEFT JOIN `tabStock Entry Child` chi ON
        chi.parent = par.name
    LEFT JOIN `tabRaw Material Only` raw ON
        chi.raw_material = raw.name
    LEFT JOIN  tabVendor tv ON
        par.vendor = tv.name
    """
    where_cond = f" WHERE par.date between '{conditions['from_date_filter']}' AND '{conditions['to_date_filter']}' "

    if "branch_filter" in conditions:
        where_cond = where_cond + f" AND par.branch = '{conditions['branch_filter']}' "
    if "raw_material_filter" in conditions:
        where_cond = where_cond + f" AND chi.raw_material = '{conditions['raw_material_filter']}' "
    if "vendor_filter" in conditions:
        where_cond = where_cond + f" AND par.vendor = '{conditions['vendor_filter']}' "
    if "bill_date_filter" in conditions:
        where_cond = where_cond + f" AND par.bill_date = '{conditions['bill_date_filter']}' "
    if "ref_no_filter" in conditions:
        where_cond = where_cond + f" AND ref_no LIKE '%{conditions['ref_no_filter']}%' "
    if "remarks_filter" in conditions:
        where_cond = where_cond + f" AND par.remarks LIKE '%{conditions['remarks_filter']}%' "
    if "raw_material_like_filter" in conditions:
        where_cond = where_cond + f" AND raw.item LIKE '%{conditions['raw_material_like_filter']}%' "

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
