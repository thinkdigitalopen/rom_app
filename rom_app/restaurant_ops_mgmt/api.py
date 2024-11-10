import frappe
from datetime import datetime, timedelta
from . import utils
from frappe.utils import getdate, formatdate


@frappe.whitelist()
def testapi():
    return "test api returned"


@frappe.whitelist()
def get_date_for_report_filter():
    today = datetime.today().date()
    previous_date = today - timedelta(days=1)
    print("Today's date:", today)
    print("Previous date:", previous_date)
    print(" *************************************** ")
    # today_str = today.strftime("%d-%m-%Y")
    # previous_date_str = previous_date.strftime("%d-%m-%Y")
    # date_obj = {
    #     'today': today_str,
    #     'previous_date': previous_date_str
    #            }
    date_obj = {
        'today': today,
        'previous_date': previous_date
               }
    print("get_date_for_report_filter date:", date_obj)
    return date_obj


@frappe.whitelist()
def get_fb_opening_checklist_child(branch_param):
    print('get_fb_opening_checklist_child =======', branch_param)
    parent = frappe.qb.DocType("FB Opening Checklist Template")
    child = frappe.qb.DocType("FB Opening Checklist Template Child")
    # branch = frappe.qb.DocType("Branch")
    query = (
        frappe.qb.from_(parent)
        .inner_join(child)
        .on(parent.name == child.parent)
        .select(parent.name, parent.branch, child.question, child.name)
        .where(parent.branch == branch_param)
    )
    sql_text = query.get_sql()
    print(sql_text)
    result = query.run()
    return result


@frappe.whitelist()
def get_fb_closing_checklist_child(branch_param):
    parent = frappe.qb.DocType("FB Closing Checklist Template")
    child = frappe.qb.DocType("FB Closing Checklist Template Child")

    query = (
        frappe.qb.from_(parent)
        .inner_join(child)
        .on(parent.name == child.parent)
        .select(parent.name, parent.branch, child.question)
        .where(parent.branch == branch_param)
    )

    result = query.run()
    return result


@frappe.whitelist()
def get_op_opening_checklist_child(branch_param):
    parent = frappe.qb.DocType("Op Opening Checklist Template")
    child = frappe.qb.DocType("Op Opening Checklist Template Child")
    query = (
        frappe.qb.from_(parent)
        .inner_join(child)
        .on(parent.name == child.parent)
        .select(parent.name, parent.branch, child.area, child.question)
        .where(parent.branch == branch_param)
     )
    result = query.run()
    return result


@frappe.whitelist()
def get_op_closing_checklist_child(branch_param):
    parent = frappe.qb.DocType("Op Closing Checklist Template")
    child = frappe.qb.DocType("Op Closing Checklist Template Child")
    query = (
        frappe.qb.from_(parent)
        .inner_join(child)
        .on(parent.name == child.parent)
        .select(parent.name, parent.branch, child.question)
        .where(parent.branch == branch_param)
    )
    result = query.run()
    return result


@frappe.whitelist()
def testapi2():
    # result = frappe.db.get_list(
    #     "Chef Opening Checklist Template",
    #     filters={"chef_open_template_branch": 1},
    #     fields=["name", "chef_open_template_branch"],
    #     as_list=True,
    # )
    result = frappe.db.get_list(
        "Chef Closing Checklist Template",
        filters={"chef_close_template_branch": 2},
        fields=["name", "chef_close_template_branch"],
        as_list=True,
    )
    return result


@frappe.whitelist()
def get_the_branch_for_the_user(emailid):
    branch = utils.find_user_branch()
    current_date = datetime.today().date()
    result = {
            "branch": branch,
            "current_date": current_date
            }
    return result


@frappe.whitelist()
def get_the_branch_for_the_user_based_on_email_id(emailid):
    branch = utils.find_user_branch_based_on_email(emailid)
    current_date = datetime.today().date()
    print("^^^^^^^^^^^^^^^^^^^^")
    print(current_date)
    # today_date = getdate()
    current_date = utils.format_date_based_on_system_settings(current_date)
    # print(today_date)
    seven_dates = utils.get_seven_dates_from_current_date()
    result = {
            "branch": branch,
            "current_date": current_date,
            'seven_dates': seven_dates
            }
    return result


@frappe.whitelist()
def check_the_user_has_the_selected_dept_role(emailid, department_id):
    print('emailid ', emailid)
    print('department_id ', department_id)
    branch = utils.find_user_branch_based_on_email(emailid)
    print('branch <><> ', branch)

    if (branch is None):
        multi_branch_support = check_user_has_multi_branch_support(emailid)
        if (multi_branch_support is True):
            return True
        return False

    build_sql = """
    SELECT
        td.role
    FROM
        tabDepartment td
    WHERE
        td.branch = '{branch}' AND td.name = '{department_id}'
    """
    build_sql = build_sql.replace("{branch}", branch)
    build_sql = build_sql.replace("{department_id}", department_id)
    print("-------- full sql ------------")
    print(build_sql)
    data = frappe.db.sql(build_sql, as_dict=True)
    dept_role = data[0].role
    print('dept_role ', dept_role)
    user_roles = frappe.get_roles(frappe.session.user)
    print(type(user_roles))
    print(user_roles)
    role_count = user_roles.count(dept_role)
    if (role_count > 0):
        print('found_role ', role_count)
        return True
    else:
        print('not found_role ')
    return False
    # user_has_chef_role = user_roles.count('Rom_Chef_Role')
    # print('============================')
    # print(user_roles)
    # print(user_has_chef_role)
    # print('self.rm_approval')
    # print(self.rm_approval)
    # print(type(self.rm_approval))
    # if (user_has_chef_role >= 1):
    #     print('user_has_chef_role >= 1')
    #     if (self.rm_approval == 1):
    #         print('self.rm_approval == 1')
    #         frappe.throw("Editing approved record is not permitted")
    # return data


# @frappe.whitelist()
# def get_the_branch_name_for_the_user2(emailid):
#     branch_id = "1"
#     branch_name = "name"
#     result = {branch_id, branch_name}
#     return result


@frappe.whitelist()
def get_chef_production_checklist_child_briyani(branch_param):
    parent = frappe.qb.DocType("Chef Production Temp")
    child = frappe.qb.DocType("Chef Prod Child Briyani Temp")

    query = (
        frappe.qb.from_(parent)
        .inner_join(child)
        .on(parent.name == child.parent)
        .select(parent.name, parent.branch, child.briyani_category, child.rateportion)
        .where(parent.branch == branch_param)
    )

    result = query.run()
    return result


@frappe.whitelist()
def get_chef_production_checklist_child_chicken(branch_param):
    parent = frappe.qb.DocType("Chef Production Temp")
    child = frappe.qb.DocType("Chef Prod Child Chicken Temp")

    query = (
        frappe.qb.from_(parent)
        .inner_join(child)
        .on(parent.name == child.parent)
        .select(parent.name, parent.branch, child.chicken_category, child.rateportion)
        .where(parent.branch == branch_param)
    )

    result = query.run()
    return result


def check_user_has_multi_branch_support(user_email):
    multi_branch_support_user = frappe.db.get_value('Rom Settings',
                                     {'settings_name': 'MultiBranchSupportUser'},
                                     ['settings_value'])
    print('multi_branch_support_user ---> ', multi_branch_support_user)
    if (len(multi_branch_support_user) > 0):
        return True
    return False

# @frappe.whitelist()
# def get_chef_production_checklist_child_chicken(branch_param):
#     parent = frappe.qb.DocType("Chef Production Temp")
#     child = frappe.qb.DocType("Chef Prod Child Chicken Temp")
#
#     query = (
#         frappe.qb.from_(parent)
#         .inner_join(child)
#         .on(parent.name == child.parent)
#         .select(parent.name, parent.branch, child.chicken_category, child.uom, child.rate)
#         .where(parent.branch == branch_param)
#     )
#
#     result = query.run()
#     return result


# @frappe.whitelist()
# def get_asset_master_child(branch_param):
#     parent = frappe.qb.DocType("Asset Master")
#     child = frappe.qb.DocType("Asset Master Child")
#
#     query = (
#         frappe.qb.from_(parent)
#         .inner_join(child)
#         .on(parent.name == child.parent)
#         .select(parent.name, parent.branch, child.category, child.item, child.standard_stock)
#         .where(parent.branch == branch_param)
#     )
#
#     result = query.run()
#     return result
#

# @frappe.whitelist()
# def get_asset_master_child_category_text(branch_param):
#     branch_param = 1
#     parent = frappe.qb.DocType("Asset Master")
#     child = frappe.qb.DocType("Asset Master Child")
#     superchild = frappe.qb.DocType("Category")
#
#     query = (
#         frappe.qb.from_(parent)
#         .inner_join(child)
#         .on(parent.name == child.parent)
#         .inner_join(superchild)
#         .on(child.category == superchild.name)
#         .select(parent.name, parent.branch, child.category, child.item, child.standard_stock, superchild.category_name)
#         .where(parent.branch == branch_param)
#     )
#
#     result = query.run()
#     return result

@frappe.whitelist()
def get_asset_master_child_based_on_branch_category(branch_param, category_param):
    # branch_param = 1
    # category_param = 1
    parent = frappe.qb.DocType("Asset Master")
    child = frappe.qb.DocType("Asset Master Child")

    query = (
        frappe.qb.from_(parent)
        .inner_join(child)
        .on(parent.name == child.parent )
        .select(parent.branch, child.category, child.item, child.standard_stock)
        .where(child.category == category_param )
        .where(parent.branch == branch_param)
    )

    result = query.run()
    # sql_text = query.get_sql()
    # print(sql_text)
    return result


@frappe.whitelist()
def get_asset_master_singltable_child_based_on_branch(branch_param):
    parent = frappe.qb.DocType("Asset Master")
    child = frappe.qb.DocType("Asset Master Group")
    print("branch_param")
    print(branch_param)
    # print(category_param)
    # child = frappe.qb.DocType("Asset Master Child")
    query = (
        frappe.qb.from_(parent)
        .left_join(child)
        .on(parent.asset_group == child.name)
        .select(parent.branch, parent.category, parent.item,
                parent.standard_stock,
                child.group_name, parent.name, parent.attach_image,
                child.name.as_('asset_group_id')
                )
        .where(parent.branch == branch_param)
            )
    result = query.run()
    sql_text = query.get_sql()
    print(sql_text)
    return result


@frappe.whitelist()
def get_production_items():
    sql_briyani = " (SELECT  child1.briyani_category as item FROM `tabChef Prod Child Briyani Temp` child1) "
    sql_chicken = " (SELECT  child2.chicken_category as item FROM `tabChef Prod Child Chicken Temp` child2) "
    sql_full = sql_briyani + "  UNION  " + sql_chicken
    print(sql_full)
    item_data = frappe.db.sql(sql_full, as_dict=0)
    return item_data
    print(item_data)


@frappe.whitelist()
def get_production_item_query_briyani(doctype, txt, searchfield, start, page_len, filters):
    print("python")
    sql = """
    select briyani_category, name from `tabChef Prod Child Briyani Temp`
    """
    result = frappe.db.sql(sql)
    print(result)
    return result


@frappe.whitelist()
def get_production_item_query_chicken(doctype, txt, searchfield, start, page_len, filters):
    print("python")
    sql = """
    select chicken_category, name from `tabChef Prod Child Chicken Temp`
    """
    result = frappe.db.sql(sql)
    print(result)
    return result


@frappe.whitelist()
def update_database_usage():
    current_time = datetime.today()
    print('================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print(current_time)
    doc = frappe.get_doc({
        'doctype': 'Task',
        'title': current_time
    })
    doc.insert()
    frappe.db.commit()


@frappe.whitelist()
def get_rm_closing_checklist_child(branch_param):
    parent = frappe.qb.DocType("RM Closing Checklist Template")
    child = frappe.qb.DocType("RM Closing Checklist Template Child")

    query = (
        frappe.qb.from_(parent)
        .inner_join(child)
        .on(parent.name == child.parent)
        .select(parent.name, parent.branch, child.question)
        .where(parent.branch == branch_param)
    )

    result = query.run()
    return result
