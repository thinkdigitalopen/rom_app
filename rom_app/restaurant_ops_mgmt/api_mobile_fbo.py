import frappe
from datetime import datetime
import json
from . import api


@frappe.whitelist()
def get_fb_opening_checklist_child_mobile(branch_param):
    print('get_fb_opening_checklist_child_mobile =======', branch_param)
    print("-------- get data ------------")
    current_date = datetime.today().date()
    build_sql = """
    SELECT
        coc.name as parent_name,
        coc.date,
        coc.user_name,
        coc.branch,
        cocc.name as child_name,
        cocc.audit,
        cocc.question
    FROM
        `tabFB Opening Checklist` coc
        JOIN `tabFB Opening Checklist Child` cocc
    ON
        coc.name = cocc.parent
    """
    where_cond_date = f" DATE(coc.date) =  '{current_date}'"
    where_cond_branch = f" coc.branch =  '{branch_param}'"
    build_sql = f"{build_sql} WHERE {where_cond_date} AND {where_cond_branch}"
    print("-------- full sql ------------")
    print(build_sql)
    data = frappe.db.sql(build_sql, as_dict=True)
    print(data)
    return data


@frappe.whitelist()
def update_fb_opening_checklist_child_mobile(form_values):
    print('update_fb_opening_checklist_child_mobile =======', form_values)
    json_object = json.loads(form_values)
    print(type(json_object))
    field_parent_name = json_object["field_parent_name"]
    print(field_parent_name)
    for x in json_object:
        print(x, " -> ", json_object[x])
#   User
    field_user = json_object["field_user"]
    field_user = split_by_colon(field_user)
    print(field_user)
#   Branch
    field_branch = json_object["field_branch"]
    field_branch = split_by_colon(field_branch)
    print(field_branch)
#   Date
    field_current_date = json_object["field_current_date"]
    field_current_date = split_by_colon(field_current_date)
    print(field_current_date)
#   Parent Id
    field_parent_name = json_object["field_parent_name"]
    field_parent_name = split_by_colon(field_parent_name)
    print(field_parent_name)

    # remove non row values from dict

    json_object.pop('field_user', None)
    json_object.pop('field_branch', None)
    json_object.pop('field_current_date', None)
    json_object.pop('field_parent_name', None)

    for x in json_object:
        print(x, " <-> ", json_object[x])

    parent_doc = frappe.get_doc("FB Opening Checklist", field_parent_name)
    print(parent_doc)
    for q in parent_doc.questions:
        disp = f"name {q.name}  = qaudit  {q.audit} = qquestion  {q.question}"
        print(disp)
        child_name = q.name
        print('child_name', child_name)
        value_from_user = json_object[str(child_name)]
        print('value_from_user', value_from_user)
        if (value_from_user == 1):
            q.audit = 1
        else:
            q.audit = 0
        q.save()
    parent_doc.db_update()
    frappe.db.commit()


@frappe.whitelist()
def fb_opening_check_today_record_exits_otherwise_create_one(branch,
                                                             current_date,
                                                             email_id,
                                                             user_name):
    print('fb_opening_check_today_record_exits_otherwise_create_one ~~')
    print('branch ', branch)
    print('current_date ', current_date)
    print('email_id ', email_id)
    print('user_name ', user_name)
    parent_name = 0
    parent_name = fb_opening_check_today_record_exist(branch,
                                                      user_name,
                                                      current_date)
    print('parent_name1 ', parent_name)
    if (parent_name == 0):
        parent_name = fb_opening_insert_today_records(branch,
                                                      current_date,
                                                      email_id,
                                                      user_name)
    print('parent_name2 ', parent_name)
    return parent_name


def fb_opening_check_today_record_exist(branch, user_name, current_date):
    print('fb_opening_check_today_record_exist')
    # current_date = datetime.today().date()
    rec_count = frappe.db.count("FB Opening Checklist", filters={
            'user_name': user_name,
            'branch': branch,
            'date': current_date
        })

    print('*** rec_count ', rec_count)
    if (rec_count > 0):
        print(" *** record_exists")
        parent_rec = frappe.get_last_doc('FB Opening Checklist', filters={
            'user_name': user_name,
            'branch': branch,
            'date': current_date
        })
        print(parent_rec)
        print(parent_rec.name)
        return parent_rec.name

    print(" *** record_does_not_exists")
    record_not_exists = 0
    return record_not_exists


def fb_opening_insert_today_records(branch, current_date,
                                    email_id, user_name):
    print('fb_opening_insert_today_records')
    print('branch-', branch)
    print('current_date-', current_date)
    print('email_id-', email_id)
    print('user_name-', user_name)
    print("^^^^^^^^^^^^^^^^^")
    parent = frappe.new_doc('FB Opening Checklist')
    parent.branch = branch
    parent.date = current_date
    parent.user_name = user_name
    parent.save(ignore_permissions=True)

    parent_new = frappe.get_last_doc('FB Opening Checklist',
                                     filters={"branch": branch,
                                              "user_name": user_name,
                                              "date": current_date
                                              })
    print(parent_new)
    print(parent_new.name)
    # Create child entries for the parent
    q_template = api.get_fb_opening_checklist_child(branch)
    print('q_template')
    print(q_template)
    print('====== q_template item =============')
    for item in q_template:
        print(item)
        template_question = item[2]
        child = frappe.get_doc({
            'doctype': 'FB Opening Checklist Child',
            'parent': parent_new.name,
            'parentfield': 'questions',
            'parenttype': 'FB Opening Checklist',
            'audit': 0,
            'question': template_question,
        })
        child.insert(ignore_permissions=True)
    return parent_new.name


def get_fb_opening_checklist_template_child_mobile(branch_param):
    print('get_fb_opening_checklist_template_child_mobile ====', branch_param)
    print("-------- get data ------------")
    current_date = datetime.today().date()
    build_sql = """
    SELECT
        coc.name as parent_name,
        coc.date,
        coc.user_name,
        coc.branch,
        cocc.name as child_name,
        cocc.audit,
        cocc.question
    FROM
        `tabFB Opening Checklist` coc
        JOIN `tabFB Opening Checklist Child` cocc
    ON
        coc.name = cocc.parent
    """
    where_cond_date = f" DATE(coc.date) =  '{current_date}'"
    where_cond_branch = f" coc.branch =  {branch_param}"
    build_sql = f"{build_sql} WHERE {where_cond_date} AND {where_cond_branch}"
    print("-------- full sql ------------")
    print(build_sql)
    data = frappe.db.sql(build_sql, as_dict=True)
    print(data)
    return data


def split_by_colon(full_data):
    all_data = full_data.split(':')
    actual_value = all_data[1]
    actual_value = actual_value.strip()
    return actual_value
