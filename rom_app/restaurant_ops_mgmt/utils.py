import frappe
from datetime import datetime, timedelta
from frappe.utils import getdate, formatdate


def find_session_user_email():
    user_email = frappe.session.user
    return user_email


def find_user_branch():
    user_email = frappe.session.user
    sql = """
       SELECT for_value
       FROM `tabUser Permission` tup
       WHERE user  = '{}';
    """
    sql = sql.format(user_email)
    # print(sql)
    item_data = frappe.db.sql(sql, as_dict=0)
    res_length = len(item_data)
    # print(res_length)
    # print(item_data)
    return item_data[0][0]


def find_user_branch_based_on_email(email):
    sql = """
       SELECT for_value
       FROM `tabUser Permission` tup
       WHERE user  = '{}';
    """
    sql = sql.format(email)
    # print(sql)
    item_data = frappe.db.sql(sql, as_dict=0)
    res_length = len(item_data)
    # print(res_length)
    # print(item_data)
    if (res_length == 0):
        return None
    return item_data[0][0]


def is_user_an_administrator():
    roles = frappe.get_roles(frappe.session.user)
    # print(roles)
    if "Administrator" in roles:
        return True
    return False


def get_seven_dates_from_current_date():
    seven_dates = []
    # current_date = datetime.today().date()
    current_date = getdate()
    date_format = frappe.get_system_settings('date_format')
    # # print('current_date ', formatted_date)
    seven_dates.append(formatdate(current_date, date_format))
    for x in range(6):
        y = x + 1
        # print(y)
        one_day_before = current_date - timedelta(days=y)
        formatted_date = formatdate(one_day_before, date_format)
        seven_dates.append(str(formatted_date))
    # print('seven_dates ', seven_dates)
    return seven_dates


def format_date_based_on_system_settings(date_input):
    date_format = frappe.get_system_settings('date_format')
    formatted_date = formatdate(date_input, date_format)
    return formatted_date


def format_date_from_Ydm_to_Ymd(date_input):
    formatted_date = datetime.strptime(date_input, '%Y-%d-%m').strftime('%Y-%m-%d')
    return formatted_date

def format_date_from_dmY_to_Ymd(date_input):
    formatted_date = datetime.strptime(date_input, '%d-%m-%Y').strftime('%Y-%m-%d')
    return formatted_date
