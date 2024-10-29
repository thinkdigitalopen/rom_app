import frappe
from . import utils


@frappe.whitelist()
def get_opening_tickets():
    print('get_opening_tickets - number card =======')
    print('=================================== =======')
    if (frappe.session.user == 'Administrator'):
        ret_val = {"value": 0}
        return ret_val
    email_param = utils.find_session_user_email()
    branch_param = utils.find_user_branch_based_on_email(email_param)
    print('email =======', email_param)
    print('branch_param =======', branch_param)
    print("-------- get data ------------")
    open_tickts_count = get_op_opening_tickets(email_param, branch_param)
    ret_val = {"value": open_tickts_count}
    return ret_val


def get_op_opening_tickets(email, branch):
    print('get_op_opening_tickets - number card =======')
    print('=================================== =======')
    # ---- roles
    user_roles = frappe.get_roles(frappe.session.user)
    print(type(user_roles))
    print(user_roles)
    user_role = find_the_current_user_role()
    depts = find_all_departments_for_user_role(user_role)
    depts_sql = format_the_department_list_for_sql(depts)
    print("**************** user role ********")
    print(user_role)
    build_sql = """
    SELECT
        count(*) as count
    FROM
        `tabTicket Report` tick
    WHERE
    tick.completed = 0 AND
    tick.Branch = '{branch}' AND
    tick.department IN ({departments})
    """
    build_sql = build_sql.replace("{branch}", branch)
    build_sql = build_sql.replace("{departments}", depts_sql)
    print(build_sql)
    data = frappe.db.sql(build_sql, as_dict=True)
    count = data[0].count
    return count


def find_the_current_user_role():
    user_roles = frappe.get_roles(frappe.session.user)
    print(type(user_roles))
    print(user_roles)

    if any(x == 'Rom_FB_Role' for x in user_roles):
        return 'Rom_FB_Role'

    if any(x == 'Rom_Op_Role' for x in user_roles):
        return 'Rom_Op_Role'

    if any(x == 'Rom_Cash_Role' for x in user_roles):
        return 'Rom_Cash_Role'

    if any(x == 'Rom_Store_Role' for x in user_roles):
        return 'Rom_Store_Role'

    if any(x == 'Rom_HR_Role' for x in user_roles):
        return 'Rom_HR_Role'

    return ''


def find_all_departments_for_user_role(user_role):
    build_sql = """
    SELECT
         name
    FROM
        `tabDepartment` dept
    WHERE
    dept.Role = '{user_role}'
    """
    build_sql = build_sql.replace('{user_role}', user_role)
    print(build_sql)
    data = frappe.db.sql(build_sql, as_dict=True)
    print(data)
    print("dt -=-===-==")
    print(type(data))
    return data


def format_the_department_list_for_sql(depts):
    uuids = [dept['name'] for dept in depts]
    depts_sql = str(uuids)[1:-1]
    print(depts_sql)
    return depts_sql
