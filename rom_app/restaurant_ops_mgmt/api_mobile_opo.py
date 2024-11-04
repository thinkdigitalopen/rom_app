import frappe
import json
from . import api
from . import utils


@frappe.whitelist()
def get_op_opening_checklist_child_mobile_area(branch_param, area_param, load_date):
    print(' =======', branch_param, area_param, load_date)
    print("-------- get data ------------")
    # current_date = datetime.today().date()
    print('load_date ', load_date)
    load_date = utils.format_date_from_dmY_to_Ymd(load_date)
    print(' utils.format_date_from_dmY_to_Ymd(load_date) ', load_date)

    build_sql = """
    SELECT
        coc.name as parent_name,
        coc.date,
        coc.user_name,
        coc.branch,
        cocc.name as child_name,
        cocc.audit,
        cocc.area,
        cocc.question
    FROM
        `tabOp Opening Checklist` coc
        JOIN `tabOp Opening Checklist Child` cocc
    ON
        coc.name = cocc.parent
    """
    where_cond_date = f" DATE(coc.date) =  '{load_date}'"
    where_cond_branch = f" coc.branch =  '{branch_param}'"
    where_cond_area = f" cocc.area =  '{area_param}'"
    build_sql = f"{build_sql} WHERE {where_cond_date} AND {where_cond_branch} AND {where_cond_area}"
    print("-------- full sql ------------")
    print(build_sql)
    data = frappe.db.sql(build_sql, as_dict=True)
    print(data)
    return data


@frappe.whitelist()
def get_distinct_area_for_branch(branch_param):
    print('get_distinct_area_for_branch ------', branch_param)
    print("-------- get data ------------")
    build_sql = """
    SELECT
    DISTINCT cocc.area
    FROM
    `tabOp Opening Checklist Template` coc
    JOIN `tabOp Opening Checklist Template Child` cocc
    ON
    coc.name = cocc.parent
    """
    where_cond_branch = f" AND coc.branch =  '{branch_param}'"
    build_sql = f"{build_sql} {where_cond_branch}"
    print("-------- full sql ------------")
    print(build_sql)
    data = frappe.db.sql(build_sql, as_dict=True)
    print(data)
    return data


@frappe.whitelist()
def update_op_opening_checklist_child_mobile(form_values):
    print('<< =======', form_values)
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

    parent_doc = frappe.get_doc("Op Opening Checklist", field_parent_name)
    print(parent_doc)
    for q in parent_doc.questions:
        disp = f"name {q.name}  = qaudit  {q.audit} = qquestion  {q.question}"
        print(disp)
        child_name = q.name
        print('child_name -=-= ', child_name)
        found_it = check_value_exists_in_object(child_name, json_object)
        if (found_it is True):
            print('found it -> ', child_name)
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
def op_opening_check_record_exits_otherwise_create_one(branch,
                                                       current_date,
                                                       email_id,
                                                       user_name,
                                                       load_date):
    print('~~~> ~~~> ~~~>  ')
    print('branch ', branch)
    print('current_date ', current_date)
    print('email_id ', email_id)
    print('user_name ', user_name)
    print('load_date ', load_date)
    load_date = utils.format_date_from_dmY_to_Ymd(load_date)
    print(' utils.format_date_from_dmY_to_Ymd(load_date) ', load_date)

    parent_name = 0
    parent_name = op_opening_check_today_record_exist(branch,
                                                      user_name,
                                                      load_date)
    print('parent_name1 ', parent_name)
    if (parent_name == 0):
        parent_name = op_opening_insert_today_records(branch,
                                                      current_date,
                                                      email_id,
                                                      user_name,
                                                      load_date)
    print('parent_name2 ', parent_name)
    ret_val = {'parent_name': parent_name}
    print(ret_val)
    return ret_val


def op_opening_check_today_record_exist(branch, user_name, load_date):
    print('()()------')
    rec_count = frappe.db.count("Op Opening Checklist", filters={
            'user_name': user_name,
            'branch': branch,
            'date': load_date
        })

    print('*** rec_count ', rec_count)
    if (rec_count > 0):
        print(" *** record_exists")
        parent_rec = frappe.get_last_doc('Op Opening Checklist', filters={
            'user_name': user_name,
            'branch': branch,
            'date': load_date
        })
        print(parent_rec)
        return parent_rec.name

    print(" *** record_does_not_exists")
    record_not_exists = 0
    return record_not_exists


def op_opening_insert_today_records(branch, current_date,
                                    email_id, user_name, load_date):
    print(' _____')
    print(type(load_date))
    print('branch-', branch)
    print('current_date-', current_date)
    print('email_id-', email_id)
    print('user_name-', user_name)
    print('load_date-', load_date)
    print("^^^^^^^^^^^^^^^^^")
    parent = frappe.new_doc('Op Opening Checklist')
    parent.branch = branch
    parent.date = load_date
    parent.user_name = user_name
    parent.save(ignore_permissions=True)
    print("^^^^^^^$$$$$^^^^^^^^^^")
    parent_new = frappe.get_last_doc('Op Opening Checklist',
                                     filters={"branch": branch,
                                              "user_name": user_name,
                                              "date": load_date
                                              })
    print(parent_new)
    print(parent_new.name)
    # Create child entries for the parent
    q_template = api.get_op_opening_checklist_child(branch)
    print('q_template')
    print(q_template)
    print('====== q_template item =============')
    for item in q_template:
        print(item)
        template_area = item[2]
        template_question = item[3]
        child = frappe.get_doc({
            'doctype': 'Op Opening Checklist Child',
            'parent': parent_new.name,
            'parentfield': 'questions',
            'parenttype': 'Op Opening Checklist',
            'audit': 0,
            'area': template_area,
            'question': template_question,
        })
        child.insert(ignore_permissions=True)
    return parent_new.name


def split_by_colon(full_data):
    all_data = full_data.split(':')
    actual_value = all_data[1]
    actual_value = actual_value.strip()
    return actual_value


def check_value_exists_in_object(child_name, area_dict):
    child_name_str = str(child_name)
    found = area_dict.get(child_name_str)
    if (found is None):
        return False
    return True
