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
            'user_name': d.user_name,
            'branch': d.branch,
            'expense_desc': d.expense_desc,
            'expense_amount': d.expense_amount,
            'responsible_person': d.responsible_person,
            'remarks': d.remarks,
        })
        data.append(row)

    return columns, data


def get_columns():
    return [
        {
            'fieldname': 'name',
            'label': 'Id',
            'fieldtype': 'Link',
            'options': 'Expense Report',
        },
        {
            'fieldname': 'date',
            'label': 'Date',
            'fieldtype': 'Data',
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
            'fieldname': 'expense_desc',
            'label': 'Expense Desc',
            'fieldtype': 'Link',
            'options': 'Expense Desc Template',
        },
        {
            'fieldname': 'expense_amount',
            'label': 'Expense Amount',
            'fieldtype': 'Data',
        },
        {
            'fieldname': 'responsible_person',
            'label': 'Res. person',
            'fieldtype': 'Link',
            'options': 'Responsible Person Template',
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
    expense.name,
    expense.date,
    expense.user_name,
    expense.branch,
    exptemp.expense_desc as expense_desc,
    expense.expense_amount,
    resptemp.person_name as responsible_person,
    expense.remarks
    FROM `tabExpense Report` expense
    INNER JOIN `tabExpense Desc Template` exptemp
    ON expense.expense_desc = exptemp.name
    INNER JOIN `tabResponsible Person Template` resptemp
    ON expense.responsible_person = resptemp.name
        """
    where_cond = f" WHERE expense.date between '{conditions['from_date_filter']}' AND '{conditions['to_date_filter']}' "

    if "branch_filter" in conditions:
        where_cond = where_cond + f" AND expense.branch = '{conditions['branch_filter']}' "
    if "expense_desc_filter" in conditions:
        where_cond = where_cond + f" AND expense.expense_desc = '{conditions['expense_desc_filter']}' "
    if "responsible_person_filter" in conditions:
        where_cond = where_cond + f" AND expense.responsible_person = '{conditions['responsible_person_filter']}' "

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


@frappe.whitelist()
def get_data_by_count(filters):
    conditions = get_conditions(filters)
    print("-------- get data ------------")
    print(conditions)
    build_sql = """
    SELECT
    expense.date as date,
    sum(expense.expense_amount) as amount
    FROM
    `tabExpense Report` expense
        """
    where_cond = f" WHERE expense.date between '{conditions['from_date_filter']}' AND '{conditions['to_date_filter']}' "

    if "branch_filter" in conditions:
        where_cond = where_cond + f" AND expense.branch = '{conditions['branch_filter']}' "

    group_by = " GROUP By date "
    order_by = " ORDER BY date DESC "
    build_sql = f"{build_sql}  {where_cond} {group_by} {order_by}"

    print("-------- full sql ------------")
    print(build_sql)
    data = frappe.db.sql(build_sql, as_dict=True)
    print(data)
    return data
