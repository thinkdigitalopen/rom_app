import frappe
import yaml


def execute(filters=None):
    print("=========  SampleDocReport  ================")
    print(yaml.dump(filters))
    data, columns = [], []
    columns = get_columns()
    cs_data = get_data(filters)

    data = []
    for d in cs_data:
        row = frappe._dict({
            'name': d.name,
            'full_name': d.full_name,
            'city': d.city,
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
            'options': 'SampleDoc',
        },
        {
            'fieldname': 'full_name',
            'label': 'Full Name',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'city',
            'label': 'City',
            'fieldtype': 'Data',
        },
    ]


def get_data(filters):
    build_sql = """
    SELECT tsd.name, tsd.full_name, tsd.city from tabSampleDoc tsd;
        """
    print("-------- full sql ------------")
    print(build_sql)
    data = frappe.db.sql(build_sql, as_dict=True)
    print(data)
    return data

