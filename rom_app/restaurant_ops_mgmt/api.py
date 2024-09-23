import frappe
from datetime import datetime
import json


@frappe.whitelist()
def get_chef_opening_checklist_child(branch_param):
    parent = frappe.qb.DocType("Chef Opening Checklist Template")
    child = frappe.qb.DocType("Chef Opening Checklist Template Child")

    query = (
        frappe.qb.from_(parent)
        .inner_join(child)
        .on(parent.name == child.parent)
        .select(parent.name, parent.chef_open_template_branch, child.template_question)
        .where(parent.chef_open_template_branch == branch_param)
    )

    result = query.run()
    return result


@frappe.whitelist()
def get_dm_opening_checklist_child(branch_param):
    parent = frappe.qb.DocType("Dm Opening Checklist Template")
    child = frappe.qb.DocType("Dm Opening Checklist Template Child")

    query = (
        frappe.qb.from_(parent)
        .inner_join(child)
        .on(parent.name == child.parent)
        .select(parent.name, parent.dm_open_template_branch, child.template_question)
        .where(parent.dm_open_template_branch == branch_param)
    )

    result = query.run()
    return result


@frappe.whitelist()
def testapi():
    return "test api returned"


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
def get_chef_closing_checklist_child(branch_param):
    parent = frappe.qb.DocType("Chef Closing Checklist Template")
    child = frappe.qb.DocType("Chef Closing Checklist Template Child")

    query = (
        frappe.qb.from_(parent)
        .inner_join(child)
        .on(parent.name == child.parent)
        .select(parent.name, parent.chef_close_template_branch, child.template_question)
        .where(parent.chef_close_template_branch == branch_param)
    )

    result = query.run()
    return result


@frappe.whitelist()
def get_dm_closing_checklist_child(branch_param):
    parent = frappe.qb.DocType("Dm Closing Checklist Template")
    child = frappe.qb.DocType("Dm Closing Checklist Template Child")

    query = (
        frappe.qb.from_(parent)
        .inner_join(child)
        .on(parent.name == child.parent)
        .select(parent.name, parent.dm_close_template_branch, child.template_question)
        .where(parent.dm_close_template_branch == branch_param)
    )

    result = query.run()
    return result

#
# @frappe.whitelist()
# def return_T_if_Chef_Opening_entry_per_day_per_user_per_branch_exist(p_username,p_branch):
#     p_username = 'chefuser1'
#     p_branch = 1
#     p_day = '2024-07-23'
#     rec_count = 0
#     p_day = datetime.today()
#
#     rec_count = frappe.db.count('Chef Opening Checklist', filters={
#         'user_name': p_username,
#         'chef_open_branch': p_branch,
#         'chef_open_date': p_day
#     }
#     )
#
#     if rec_count > 0:
#         return True
#
#     return False


@frappe.whitelist()
def get_the_branch_name_for_the_user(emailid):
    branch_id = frappe.db.get_value(
        "User to Branch Assignment",
        {"user": emailid},
        "branch"
        )

    branch_name = frappe.db.get_value(
        "Branch",
        {"name": branch_id},
        "branch_name",
        )

    result = {"branch_id": branch_id, "branch_name": branch_name}
    return result


@frappe.whitelist()
def get_the_branch_name_for_the_user2(emailid):
    branch_id = "1"
    branch_name = "name"
    result = {branch_id, branch_name}
    return result


@frappe.whitelist()
def get_chef_production_checklist_child_briyani(branch_param):
    parent = frappe.qb.DocType("Chef Production Temp")
    child = frappe.qb.DocType("Chef Prod Child Briyani Temp")

    query = (
        frappe.qb.from_(parent)
        .inner_join(child)
        .on(parent.name == child.parent)
        .select(parent.name, parent.branch, child.briyani_category, child.portion, child.rateportion)
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
        .select(parent.name, parent.branch, child.chicken_category, child.uom, child.rate)
        .where(parent.branch == branch_param)
    )

    result = query.run()
    return result


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
def get_asset_master_singltable_child_based_on_branch_category(branch_param, category_param):
    # branch_param = 1
    # category_param = 1
    parent = frappe.qb.DocType("Asset Master")
    print("branch_param")
    print(branch_param)
    print(category_param)
    # child = frappe.qb.DocType("Asset Master Child")

    query = (
        frappe.qb.from_(parent)
        .select(parent.branch, parent.category, parent.item, parent.standard_stock)
        .where(parent.category == category_param)
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

