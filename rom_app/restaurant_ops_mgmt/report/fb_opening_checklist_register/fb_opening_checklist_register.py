import frappe
import yaml
from ....restaurant_ops_mgmt import api_report


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
            'audit': d.audit,
            'question': d.question,
        })
        data.append(row)

    return columns, data


def get_columns():
    return [
        {
            'fieldname': 'name',
            'label': 'Id',
            'fieldtype': 'Link',
            'width': '80',
            'options': 'FB Opening Checklist',
        },
        {
            'fieldname': 'date',
            'label': 'Date',
            'fieldtype': 'Data',
            'width': '120'
        },
        {
            'fieldname': 'user_name',
            'label': 'User Name',
            'fieldtype': 'Data',
            'width': '140'
        },
        {
            'fieldname': 'branch',
            'label': 'Branch',
            'fieldtype': 'Data',
            'width': '140'
        },
        {
            'fieldname': 'audit',
            'label': 'Audit',
            'fieldtype': 'Data',
            'width': '110'
        },
        {
            'fieldname': 'question',
            'label': 'Question',
            'fieldtype': 'Data',
            'width': '220',
            "align": 'left',
        }
    ]


@frappe.whitelist()
def get_data(filters):
    print('filters py-0')
    print(filters)
    conditions = api_report.get_conditions(filters)
    print("-------- get data ------------")
    print(conditions)
    build_sql = ""
    if (type(filters) is str):
        build_sql = """
            SELECT
                coc.name,
                coc.date,
                coc.user_name,
                coc.branch,
                cocc.audit,
                cocc.question
            FROM `tabFB Opening Checklist` coc
            JOIN `tabFB Opening Checklist Child` cocc
            ON coc.name= cocc.parent
            """
    else:
        build_sql = """
            SELECT
                coc.name,
                coc.date,
                coc.user_name,
                coc.branch,
            CASE WHEN
                cocc.audit = 0 THEN 'No' ELSE 'Yes' END audit,
                cocc.question
            FROM `tabFB Opening Checklist` coc
            JOIN `tabFB Opening Checklist Child` cocc
            ON coc.name= cocc.parent
            """

    where_cond = f" WHERE coc.date between '{conditions['from_date_filter']}' AND  '{conditions['to_date_filter']}' "

    if "branch_filter" in conditions:
        where_cond = where_cond + f" AND coc.branch = '{conditions['branch_filter']}' "

    if "audit_filter" in conditions:
        selection_result = conditions['audit_filter']
        print(selection_result)
        if selection_result == 'Yes':
            where_cond = where_cond + " AND cocc.audit = 1 "
        elif (selection_result == 'No'):
            where_cond = where_cond + " AND cocc.audit = 0 "

    if "question_filter" in conditions:
        where_cond = where_cond + f" AND cocc.question LIKE '%{conditions['question_filter']}%' "

    build_sql = f"{build_sql}  {where_cond}"
    print("-------- full sql ------------")
    print(build_sql)
    data = frappe.db.sql(build_sql, as_dict=True)
    print(data)
    return data
