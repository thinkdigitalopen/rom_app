import frappe
from datetime import datetime
from . import utils


@frappe.whitelist()
def get_op_opening_checklist():
    print('get_op_opening_checklist - number card =======')
    if (frappe.session.user == 'Administrator'):
        ret_val = {"value": 0}
        return ret_val
    # admiistrator_role = utils.is_user_an_administrator()
    # print('admiistrator_role ', admiistrator_role)
    # if (admiistrator_role is True):
    #     ret_val = {"value": 0}
    #     return ret_val
    branch_param = utils.find_user_branch()
    print('branch_param =======', branch_param)
    current_date = datetime.today().date()
    print("-------- get data ------------")
    audit_yes = get_op_opening_checklist_audit_yes(branch_param, current_date)
    audit_total = get_op_opening_checklist_audit_total(branch_param,
                                                       current_date)
    percentage = 0
    if (audit_yes > 0 and audit_total > 0):
        percentage = (audit_yes/audit_total) * 100
        percentage = int(percentage)
    ret_val = {"value": percentage}
    return ret_val


@frappe.whitelist()
def get_op_closing_checklist():
    print('get_op_closing_checklist - number card =======')
    if (frappe.session.user == 'Administrator'):
        ret_val = {"value": 0}
        return ret_val
    # admiistrator_role = utils.is_user_an_administrator()
    # print('admiistrator_role ', admiistrator_role)
    # if (admiistrator_role is True):
    #     ret_val = {"value": 0}
    #     return ret_val
    branch_param = utils.find_user_branch()
    print('branch_param =======', branch_param)
    current_date = datetime.today().date()
    print("-------- get data ------------")
    audit_yes = get_op_closing_checklist_audit_yes(branch_param, current_date)
    audit_total = get_op_closing_checklist_audit_total(branch_param,
                                                       current_date)
    percentage = 0
    if (audit_yes > 0 and audit_total > 0):
        percentage = (audit_yes/audit_total) * 100
        percentage = int(percentage)
    ret_val = {"value": percentage}
    return ret_val


def get_op_opening_checklist_audit_yes(branch_param, current_date):
    build_sql = """
    SELECT
    count(*) as count
    FROM
        `tabOp Opening Checklist` coc
    JOIN
        `tabOp Opening Checklist Child` cocc
    ON
        coc.name = cocc.parent
    AND
        cocc.audit = 1
    """
    where_cond_date = f" DATE(coc.date) =  '{current_date}'"
    where_cond_branch = f" coc.branch =  '{branch_param}'"
    build_sql = f"{build_sql} WHERE {where_cond_date} AND {where_cond_branch}"
    print(build_sql)
    data = frappe.db.sql(build_sql, as_dict=True)
    check_rec_exists = len(data)
    print('check_rec_exists', check_rec_exists)
    audit_yes_count = 0
    if (check_rec_exists > 0):
        audit_yes_count = data[0].count
    return audit_yes_count


def get_op_opening_checklist_audit_total(branch_param, current_date):
    build_sql = """
    SELECT
    count(*) as count
    FROM
        `tabOp Opening Checklist` coc
    JOIN
        `tabOp Opening Checklist Child` cocc
    ON
        coc.name = cocc.parent
    """
    where_cond_date = f" DATE(coc.date) =  '{current_date}'"
    where_cond_branch = f" coc.branch =  '{branch_param}'"
    build_sql = f"{build_sql} WHERE {where_cond_date} AND {where_cond_branch}"
    print(build_sql)
    data = frappe.db.sql(build_sql, as_dict=True)
    check_rec_exists = len(data)
    print('check_rec_exists', check_rec_exists)
    audit_yes_count = 0
    if (check_rec_exists > 0):
        audit_yes_count = data[0].count
    return audit_yes_count


def get_op_closing_checklist_audit_yes(branch_param, current_date):
    build_sql = """
    SELECT
    count(*) as count
    FROM
        `tabOp Closing Checklist` coc
    JOIN
        `tabOp Closing Checklist Child` cocc
    ON
        coc.name = cocc.parent
    AND
        cocc.audit = 1
    """
    where_cond_date = f" DATE(coc.date) =  '{current_date}'"
    where_cond_branch = f" coc.branch =  '{branch_param}'"
    build_sql = f"{build_sql} WHERE {where_cond_date} AND {where_cond_branch}"
    print(build_sql)
    data = frappe.db.sql(build_sql, as_dict=True)
    check_rec_exists = len(data)
    print('check_rec_exists', check_rec_exists)
    audit_yes_count = 0
    if (check_rec_exists > 0):
        audit_yes_count = data[0].count
    return audit_yes_count


def get_op_closing_checklist_audit_total(branch_param, current_date):
    build_sql = """
    SELECT
    count(*) as count
    FROM
        `tabOp Closing Checklist` coc
    JOIN
        `tabOp Closing Checklist Child` cocc
    ON
        coc.name = cocc.parent
    """
    where_cond_date = f" DATE(coc.date) =  '{current_date}'"
    where_cond_branch = f" coc.branch =  '{branch_param}'"
    build_sql = f"{build_sql} WHERE {where_cond_date} AND {where_cond_branch}"
    print(build_sql)
    data = frappe.db.sql(build_sql, as_dict=True)
    check_rec_exists = len(data)
    print('check_rec_exists', check_rec_exists)
    audit_yes_count = 0
    if (check_rec_exists > 0):
        audit_yes_count = data[0].count
    return audit_yes_count
