import frappe
from datetime import datetime
import json


def find_user_branch():
    user_email = frappe.session.user
    sql = """
       SELECT for_value
       FROM `tabUser Permission` tup
       WHERE user  = '{}';
    """
    sql = sql.format(user_email)
    print(sql)
    item_data = frappe.db.sql(sql, as_dict=0)
    res_length = len(item_data)
    print(res_length)
    print(item_data)
    return item_data[0][0]


def find_user_branch_based_on_email(email):
    sql = """
       SELECT for_value
       FROM `tabUser Permission` tup
       WHERE user  = '{}';
    """
    sql = sql.format(email)
    print(sql)
    item_data = frappe.db.sql(sql, as_dict=0)
    res_length = len(item_data)
    print(res_length)
    print(item_data)
    return item_data[0][0]


def is_user_an_administrator():
    roles = frappe.get_roles(frappe.session.user)
    print(roles)
    if "Administrator" in roles:
        return True
    return False
