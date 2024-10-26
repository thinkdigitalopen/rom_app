import frappe
import pandas as pd
from datetime import datetime
import json


def get_fb_opening_checklist_from_template():
    print('get_fb_opening_checklist_child_from_template =======')
    sql = """
    SELECT
        child_template.name, child_template.question
    FROM
        `tabFB Opening Checklist Template` parent_template
    INNER JOIN
        `tabFB Opening Checklist Template Child` child_template
    ON
        parent_template.name = child_template.parent
    WHERE
        parent_template.branch = 'HPMadurai'
    """
    result = frappe.db.sql(sql)
    print(result)
    return result


def get_fb_opening_checklist():
    print('get_fb_opening_checklist_child =======')
    sql = """
    SELECT
        parent_tab.`date`, child_tab.audit
    FROM
       `tabFB Opening Checklist` parent_tab
    INNER JOIN
        `tabFB Opening Checklist Child` child_tab
    ON
        parent_tab.name = child_tab.parent
    LEFT JOIN (
        SELECT
            child_template.name, child_template.question
        FROM
            `tabFB Opening Checklist Template` parent_template
         INNER JOIN
             `tabFB Opening Checklist Template Child` child_template
        ON
            parent_template.name = child_template.parent
        WHERE
            parent_template.branch = 'HPMadurai'
             ) template
    ON
        child_tab.question_hid = template.name
    ORDER BY
        parent_tab.`date`, child_tab.name ASC
    """
    result = frappe.db.sql(sql)
    print(result)
    return result


@frappe.whitelist()
def get_checklist_matrix_data(branch, checklist_type, from_date, to_date):
    pd.set_option('display.max_columns', None)
    pd.set_option("display.max_rows", None)
    print('get_checklist_matrix_data =======')
    template = get_fb_opening_checklist_from_template()
    trans = get_fb_opening_checklist()
    df_template = pd.DataFrame.from_records(template)
    df_template.columns = ['name', 'question']

    df_trans = pd.DataFrame.from_records(trans)
    df_trans.columns = ['date', 'audit']

    print(df_template)
    print(df_trans)
    df_trans['date'] = df_trans['date'].astype(str)

    unique_date = df_trans.date.unique()
    print(unique_date)
    print(type(unique_date))
    # unique_date_list = unique_date.tolist()
    # print(unique_date_list)
    # print(type(unique_date_list))
    # unique_date_list_str = unique_date_list.strftime("%d-%m-%Y")
    # print(unique_date_list_str)
#     for item_date in unique_date:
#         df_trans_copy = df_trans.copy()
    for item_date in unique_date:
        df_trans_copy = df_trans.copy()
        # print('df_trans_copy')
        # print(df_trans_copy)
        print('item_date - ', item_date)
        no_of_column = len(df_template.columns)
        insert_column_pos = no_of_column
        print(insert_column_pos)
        df_filter = df_trans_copy.loc[df_trans_copy['date'] == item_date].copy()
        print('df_filter')
        print(df_filter)
        # value_col = pd.Series(df_filter.audit.copy())
        # df_template = df_template.assign(item_date=value_col)
        # df_template.loc[:, item_date] = value_col
        df_template.insert(insert_column_pos, item_date, list(df_filter.audit))
        # df_template.assign(item_date=df_filter.audit)
        print('each df_template')
        print(df_template)
        # df_filter.head(0)
    # for item_date in unique_date:
    #     print('unique_date', item_date)
    #     # no_of_column = len(df_template.columns)
    #     # insert_column_pos = no_of_column
    #     # print(insert_column_pos)
    #     df_filter = df_trans.loc[df_trans['date'] == item_date]
    #     print(df_filter.audit)
    #     df_template[item_date]
    #     # df_template.insert(insert_column_pos, item_date, df_filter.audit)
    print('final df_template')
    print(df_template)
    df_dict = df_template.to_dict()
    print(df_dict)
    response = json.dumps(df_dict)
    print('response')
    print(response)
    return df_dict
