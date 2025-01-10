import frappe
import pandas as pd
from datetime import datetime, timedelta


@frappe.whitelist()
def reset_inventory_summary(branch, start_date):
    current_date_time = datetime.now()
    log_text = f"reset_inventory_summary {branch} {start_date} {current_date_time}"
    # print(log_text)
    frappe.log_error("reset_inventory_summary", log_text)
    formatted_date = start_date
    # start_date.strftime("%Y-%m-%d")
    frappe.enqueue(
        inventory_summary,
        queue='long',
        p_branch=branch, p_date=formatted_date)
    return log_text


@frappe.whitelist()
def call_inventory_summary_morning():
    current_date_time = datetime.now()
    log_text = f"inv_sum morning {current_date_time}"
    # print(log_text)
    frappe.log_error("call_inventory_summary_morning", log_text)
    branch_all = frappe.get_list('Branch', pluck='name')
    # print(branch_all)
    cur_date = datetime.now()
    formatted_date = cur_date.strftime("%Y-%m-%d")
    for i, each_branch in enumerate(branch_all):
        # print(each_branch)
        frappe.enqueue(
            inventory_summary,
            queue='long',
            p_branch=each_branch, p_date=formatted_date)
    return log_text


@frappe.whitelist()
def call_inventory_summary_morning_60_days_before():
    # print('60_days_before')
    current_date_time = datetime.now()
    p_date = current_date_time - timedelta(days=63)
    p_end_date = current_date_time - timedelta(days=57)
    branch_all = frappe.get_list('Branch', pluck='name')
    for i, each_branch in enumerate(branch_all):
        log_text = f" {each_branch} {p_date} {p_end_date} "
        frappe.log_error("60_days_before ", log_text)
        frappe.enqueue(
            inventory_summary_for_start_and_end_date,
            queue='long',
            p_branch=each_branch, p_date=p_date, p_end_date=p_end_date)

    return "call_inventory_summary_morning_60_days_before completed"


@frappe.whitelist()
def inventory_summary_for_start_and_end_date_enquee(p_branch, p_date, p_end_date):
    log_text = f"inventory_summary_for_start_and_end_date_enquee {p_branch} {p_date} {p_end_date}"
    print(log_text)
    frappe.enqueue(inventory_summary_for_start_and_end_date,
                   queue='long', p_branch=p_branch, p_date=p_date, p_end_date=p_end_date)
    return log_text


@frappe.whitelist()
def inventory_summary_for_start_and_end_date(p_branch, p_date, p_end_date):
    # print("#################inventory_summary_for_start_and_end_date##########")
    # frappe.log_error("changes", log_text)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)
    # print("============= inventory_summary START DATE to END DATE >>>>>>>")
    date_format = "%Y-%m-%d"

    if isinstance(p_date, str):
        p_date = datetime.strptime(p_date, date_format).date()
    if isinstance(p_end_date, str):
        p_end_date = datetime.strptime(p_end_date, date_format).date()

    log_text = f"inventory_summary_start end -> {p_branch} {p_date} {p_end_date}"
    frappe.log_error("inventory_summary_for_start_and_end_date ", log_text)

    all_dates = collect_all_dates_between_from_and_to_date(p_date, p_end_date)
    # print('p_branch - ', p_branch)
    # print('p_date - ', p_date)
    # print('p_end_date - ', p_end_date)
    # print('all_dates - ', all_dates)

    for i, each_date in enumerate(all_dates):
        prev_date = get_previous_date(each_date)
        # print(' ===> LOOP ===============> ', i, each_date, prev_date)
        df_rm = get_raw_materials(p_branch)
        df_stock_entry = get_stock_entry(p_branch, each_date)
        df_indnets = get_indents(p_branch, each_date)
        df_wastages = get_wastages(p_branch, each_date)
        df_inventory = create_inventory_summary_empty_data_frame()
        df_inv_by_date = get_inv_sum_for_specific_date(p_branch, prev_date)

        # print(" [[0]] read dfs ***************************")
        # print('df_rm \n', df_rm)
        # print('df_stock_entry  \n', df_stock_entry)
        # print('df_indnets  \n', df_indnets)
        # print('df_wastages  \n', df_wastages)
        # print('df_inventory  \n', df_inventory)
        # print('df_inv_by_date  \n', df_inv_by_date)
        # print("************** = = = ********************")

        if (df_inv_by_date.empty):
            # print('df_inv_by_date.empty ')
            df_inventory = transfer_rm_to_inv_sum(df_inventory, df_rm, each_date)
            # print('[[1]] - after transfer_rm_to_inv_sum \n', df_inventory)
        else:
            # print('NOT df_inv_by_date.empty ')
            df_inventory = copy_prev_df_inv_to_current(df_inventory, df_inv_by_date, each_date)
            # print('[[1.5]] - copy_prev_df_inv_to_current \n', df_inventory)

        df_inventory = process_stock_entry(df_inventory, df_stock_entry)
        # print("[[2]] - after process_stock_entry  \n  ")
        # print("[[2]] - after process_stock_entry  \n  ", df_inventory)

        df_inventory = process_indents(df_inventory, df_indnets)
        # print("[[3]] - after process_indents  \n")
        # print("[[3]] - after process_indents  \n", df_inventory)

        df_inventory = process_wastages(df_inventory, df_wastages)
        # print("[[4]] - inventory after wastages  \n")
        # print("[[4]] - inventory after wastages  \n", df_inventory)

        delete_inventory_summary_of_specific_date(p_branch, each_date)
        # print("[[5]] - delete inventory summary of specific date ")

        bulk_insert_inventory_summary(df_inventory)
        # print('[[6]] bulk_insert_inventory_summary ')

        update_raw_material_table(df_inventory)
        # print("[[7]] update_raw_material_table ")
        # print("================ inventory_summary END >>>>>>>>>>>")
    log_scheduler_job('', 'Reset Inventory From To - yes', log_text)
    return "Completed"


@frappe.whitelist()
def call_inventory_summary_morning_for_today_with_one_time_db_write():
    # print('call_inventory_summary_morning_for_today_with_one_time_db_write')
    current_date_time = datetime.now()
    log_text = f"inv_sum morning {current_date_time}"
    # print(log_text)
    frappe.log_error("call_inventory_summary_morning", log_text)
    branch_all = frappe.get_list('Branch', pluck='name')
    # print(branch_all)
    cur_date = datetime.now()
    formatted_date = cur_date.strftime("%Y-%m-%d")
    for i, each_branch in enumerate(branch_all):
        # print(each_branch)
        frappe.enqueue(
            inventory_summary_one_time_db_write,
            queue='long',
            p_branch=each_branch, p_date=formatted_date)
    return log_text


@frappe.whitelist()
def inventory_summary_one_time_db_write_enquee(p_branch, p_date):
    log_text = f"inventory_summary_one_time_db_write_enquee {p_branch} {p_date}"
    print(log_text)
    frappe.enqueue(inventory_summary_one_time_db_write,
                   queue='long', p_branch=p_branch, p_date=p_date)
    return log_text


@frappe.whitelist()
def inventory_summary_one_time_db_write(p_branch, p_date):
    # last date
    current_date_time = datetime.now().date()
    # fix
    from_date_60 = current_date_time - timedelta(days=60)
    log_text = f"Branch-{p_branch} From-{from_date_60}  To-{p_date} Current-{current_date_time}"
    # print(log_text)
    frappe.log_error("inventory_summary", log_text)
    # frappe.log_error("changes", log_text)
    # print(' ^^^^^ inventory_summary ^^^^^^^^^^  ########################## ')
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)
    # print("================ inventory_summary START >>>>>>>>>>>>>>>>>")
    date_format = "%Y-%m-%d"
    if isinstance(p_date, str):
        p_date = datetime.strptime(p_date, date_format).date()
    all_dates = collect_all_dates_between_from_and_to_date(from_date_60, current_date_time)
    # print('p_branch - ', p_branch)
    # print('from_date_60 - ', from_date_60)
    # print('p_date - update date', p_date)
    # print('to date', current_date_time)
    # print('all_dates - ', all_dates)
    df_inv_memory = create_inventory_summary_empty_data_frame()

    df_rm = get_raw_materials(p_branch)
    df_stock_entry_60days = get_stock_entry_for_60_days(p_branch, from_date_60)
    df_indnets_60days = get_indents_for_60_days(p_branch, from_date_60)
    df_wastages_60days = get_wastages_for_60_days(p_branch, from_date_60)

    if (df_stock_entry_60days.empty):
        df_stock_entry_60days = create_stock_entry_empty_data_frame()
    if (df_indnets_60days.empty):
        df_indnets_60days = create_indents_empty_data_frame()
    if (df_wastages_60days.empty):
        df_wastages_60days = create_wastages_empty_data_frame()

    # print('get_raw_materials \n', df_rm)
    # print('df_stock_entry_60days \n', df_stock_entry_60days)
    # print('df_indnets_60days \n', df_indnets_60days)
    # print('df_wastages_60days \n', df_wastages_60days)

    for i, each_date in enumerate(all_dates):
        prev_date = get_previous_date(each_date)
        # print(' ===> LOOP ===============> ', i, each_date, prev_date)
        df_stock_entry = df_stock_entry_60days[df_stock_entry_60days['date'] == each_date]
        df_indnets = df_indnets_60days[df_indnets_60days['date'] == each_date]
        df_wastages = df_wastages_60days[df_wastages_60days['date'] == each_date]

        df_inventory = create_inventory_summary_empty_data_frame()
        df_inv_by_date = create_inventory_summary_empty_data_frame()

        if (each_date == from_date_60):
            # print(f'each_date == from_date_60 = {prev_date}')
            df_inv_by_date = get_inv_sum_for_specific_date(p_branch, prev_date)
            df_inv_memory = df_inv_by_date.copy()
        else:
            # print(f' df_inv_memory - each_date != from_date_60 =  {prev_date}')
            df_inv_by_date = df_inv_memory[df_inv_memory['date'] == prev_date]
        # print('df_inv_by_date \n', df_inv_by_date)
        # print(" [[0]] read dfs ***************************")
        # print('df_rm \n', df_rm)
        # print('df_stock_entry  \n', df_stock_entry)
        # print('df_indnets  \n', df_indnets)
        # print('df_wastages  \n', df_wastages)
        # print('df_inventory  \n', df_inventory)
        # print('df_inv_by_date  \n', df_inv_by_date)
        # print("************** = = = ********************")
        if (df_inv_by_date.empty):
            # print('[1.1] df_inv_by_date.empty ')
            df_inventory = transfer_rm_to_inv_sum(df_inventory, df_rm, each_date)
            # print('[[1]] - after transfer_rm_to_inv_sum \n', df_inventory)
        else:
            # print('[1.2] NOT df_inv_by_date.empty ')
            # df_inventory = copy_prev_df_inv_to_current(df_inventory, df_inv_by_date, each_date)
            df_inventory = df_inv_by_date.copy()
            # print('[1.2.1.1] - df_inv_by_date.copy() \n', df_inventory)
            # print('[1.2.1.1] -- length \n', len(df_inventory))
            # for i in range(0, len(df_inventory)):
            #     print('date  =>', i)
            #     df_inventory.loc[i, 'date'] = each_date
            for index, row in df_inventory.iterrows():
                df_inventory.at[index, 'date'] = each_date
            # print('[1.2.1] - copy_prev_df_inv_to_current \n', df_inventory)

        df_inventory = process_stock_entry(df_inventory, df_stock_entry)
        # print("[[2]] - after process_stock_entry  \n", df_inventory)
        df_inventory = process_indents(df_inventory, df_indnets)
        # print("[[3]] - after process_indents df_inventory \n", df_inventory)
        # print("[[3]] - after process_indents df_indnets \n", df_indnets)
        df_inventory = process_wastages(df_inventory, df_wastages)
        # print("[[4]] - inventory after wastages ")

        if (each_date == p_date):
            delete_inventory_summary_of_specific_date(p_branch, each_date)
            bulk_insert_inventory_summary(df_inventory)
            # print("[5]-delete invent. summary of specific date & bulk insert")

        df_inv_memory = pd.concat([df_inv_memory, df_inventory], ignore_index=True)
        # print("[[6]] - concat df - full df_inv_memory \n ")
        # print(df_inv_memory)

        if (each_date == current_date_time):
            update_raw_material_table(df_inventory)
            # print("[[7]] update_raw_material_table ")
        # print("================ inventory_summary END >>>>>>>>>>>")
    log_scheduler_job('', ' Inventory Summary Fast Update - yes', log_text)
    return "Completed"


@frappe.whitelist()
def call_inventory_summary_night():
    current_date_time = datetime.now()
    log_text = f"inv_summ night {current_date_time}"
    # print(log_text)
    frappe.log_error("call_inventory_summary_night", log_text)
    branch_all = frappe.get_list('Branch', pluck='name')
    # print(branch_all)
    cur_date = datetime.now()
    formatted_date = cur_date.strftime("%Y-%m-%d")
    for i, each_branch in enumerate(branch_all):
        # print(each_branch)
        frappe.enqueue(
            inventory_summary,
            queue='long',
            p_branch=each_branch, p_date=formatted_date)
    return log_text


@frappe.whitelist()
def inventory_summary(p_branch, p_date):
    current_date_time = datetime.now()
    log_text = f"inv_summm {p_branch} {p_date} {current_date_time}"
    # print(log_text)
    frappe.log_error("inventory_summary", log_text)
    # frappe.log_error("changes", log_text)
    # print(' ^^^^^ inventory_summary ^^^^^^^^^^  ########################## ')
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)
    # print("================ inventory_summary START >>>>>>>>>>>>>>>>>")
    date_format = "%Y-%m-%d"
    p_date = datetime.strptime(p_date, date_format).date()
    all_dates = collect_all_dates_until_today(p_date)
    # print('p_branch - ', p_branch)
    # print('p_date - ', p_date)
    # print('all_dates - ', all_dates)

    for i, each_date in enumerate(all_dates):
        prev_date = get_previous_date(each_date)
        # print(' ===> LOOP ===============> ', i, each_date, prev_date)
        df_rm = get_raw_materials(p_branch)
        df_stock_entry = get_stock_entry(p_branch, each_date)
        df_indnets = get_indents(p_branch, each_date)
        df_wastages = get_wastages(p_branch, each_date)
        df_inventory = create_inventory_summary_empty_data_frame()
        df_inv_by_date = get_inv_sum_for_specific_date(p_branch, prev_date)

        # print(" [[0]] read dfs ***************************")
        # print('df_rm \n', df_rm)
        # print('df_stock_entry  \n', df_stock_entry)
        # print('df_indnets  \n', df_indnets)
        # print('df_wastages  \n', df_wastages)
        # print('df_inventory  \n', df_inventory)
        # print('df_inv_by_date  \n', df_inv_by_date)
        # print("************** = = = ********************")

        if (df_inv_by_date.empty):
            # print('df_inv_by_date.empty ')
            df_inventory = transfer_rm_to_inv_sum(df_inventory, df_rm, each_date)
            # print('[[1]] - after transfer_rm_to_inv_sum \n', df_inventory)
        else:
            # print('NOT df_inv_by_date.empty ')
            df_inventory = copy_prev_df_inv_to_current(df_inventory, df_inv_by_date, each_date)
            # print('[[1.5]] - copy_prev_df_inv_to_current \n', df_inventory)

        df_inventory = process_stock_entry(df_inventory, df_stock_entry)
        # print("[[2]] - after process_stock_entry  \n  ", df_inventory)

        df_inventory = process_indents(df_inventory, df_indnets)
        # print("[[3]] - after process_indents  \n", df_inventory)

        df_inventory = process_wastages(df_inventory, df_wastages)
        # print("[[4]] - inventory after wastages  \n", df_inventory)

        delete_inventory_summary_of_specific_date(p_branch, each_date)
        # print("[[5]] - delete inventory summary of specific date ")

        bulk_insert_inventory_summary(df_inventory)
        # print('[[6]] bulk_insert_inventory_summary ')

        update_raw_material_table(df_inventory)
        # print("[[7]] update_raw_material_table ")
        # print("================ inventory_summary END >>>>>>>>>>>")
    log_scheduler_job('', 'Reset Inventory Summary - yes', log_text)
    return "Completed"


#  -------- 1 transfer raw material to inventory summary ------------
def transfer_rm_to_inv_sum(df_inventory, df_raw_materials, e_date):
    # df_raw_materials => name, branch, `date`, item, unit, price
    # df_inventory => branch, date, raw_material, quantity, closing_quantity, price, unit
    # columns_add = ['branch', 'date', 'raw_material', 'unit',
    # 'price', 'quantity', 'price_x_qty','closing_quantity', 'closing_amount']
    for i in range(0, len(df_raw_materials)):
        # print("-------- for loop ---------")
        branch = df_raw_materials.iloc[i]['branch']
        date = e_date
        raw_material = df_raw_materials.iloc[i]['raw_material']
        unit = df_raw_materials.iloc[i]['unit']
        price = df_raw_materials.iloc[i]['price']
        quantity = 0
        price_x_qty = 0
        closing_quantity = 0
        closing_amount = 0
        df_inventory.loc[len(df_inventory.index)] = [branch,
                                                     date,
                                                     raw_material,
                                                     unit,
                                                     price,
                                                     quantity,
                                                     price_x_qty,
                                                     closing_quantity,
                                                     closing_amount]
    return df_inventory


# ----------- 1.5 copy_ prev_df_ inventory_to_current --------------------------
def copy_prev_df_inv_to_current(df_inventory, df_inv_by_date, each_date):
    df_inventory = df_inv_by_date.copy()
    for i in range(0, len(df_inventory)):
        df_inventory.loc[i, 'date'] = each_date
    return df_inventory


# ----------- 2 process_stock_entryr --------------------------
def process_stock_entry(df_inventory, df_stock_entry):
    # branch, date, raw_material, quantity, closing_quantity, price, unit
    for i in range(0, len(df_stock_entry)):
        # print("-------- for loop --------- ", i)
        branch = df_stock_entry.iloc[i]['branch']
        raw_material = df_stock_entry.iloc[i]['raw_material']
        ord_qty = df_stock_entry.iloc[i]['ord_qty']
        pur_item_amount = df_stock_entry.iloc[i]['amount']
        df_filter = df_inventory.loc[
            (df_inventory['branch'] == branch) &
            (df_inventory['raw_material'] == raw_material)]
        #  print('!!!! process_stock_entry - df_filter  \n', df_filter)
        if (len(df_filter) == 0):
            # print('item not found in inventory ===== ')
            del_items = branch, ' -- ', raw_material, ' -- ', ord_qty, '-- ', pur_item_amount
            frappe.log_error("process_stock_entry", del_items)
            continue

        index_val = df_filter.index[0]
        quantity = df_filter.loc[index_val, 'quantity']
        price_x_qty = df_filter.loc[index_val, 'price_x_qty']
        closing_quantity = df_filter.loc[index_val, 'closing_quantity']
        closing_amount = df_filter.loc[index_val, 'closing_amount']

        total_quantity = quantity + ord_qty
        total_amount = price_x_qty + pur_item_amount

        closing_quantity = ord_qty + closing_quantity
        closing_amount = pur_item_amount + closing_amount

        df_inventory.loc[index_val, 'quantity'] = total_quantity
        df_inventory.loc[index_val, 'price_x_qty'] = total_amount
        df_inventory.loc[index_val, 'closing_quantity'] = closing_quantity
        df_inventory.loc[index_val, 'closing_amount'] = closing_amount

    return df_inventory


# ------------3 process indents --------------------------
def process_indents(df_inventory, df_indnets):
    # name  branch  raw_material  req_qty  issued_qty  date
    for i in range(0, len(df_indnets)):
        # print("-------- for loop ---------")
        branch = df_indnets.iloc[i]['branch']
        raw_material = df_indnets.iloc[i]['raw_material']
        issued_qty = df_indnets.iloc[i]['issued_qty']
        indent_item_amount = df_indnets.iloc[i]['amount']

        df_filter = df_inventory.loc[
            (df_inventory['branch'] == branch) &
            (df_inventory['raw_material'] == raw_material)]
        # print('!!!! process_indents - df_filter  \n', df_filter)

        if (len(df_filter) == 0):
            # print('item not found in inventory ===== ')
            del_items = branch, ' -- ', raw_material, ' -- ', issued_qty, '-- ', indent_item_amount
            frappe.log_error("process_indents", del_items)
            continue

        index_val = df_filter.index[0]
        quantity = df_filter.loc[index_val, 'quantity']
        price_x_qty = df_filter.loc[index_val, 'price_x_qty']
        closing_quantity = df_filter.loc[index_val, 'closing_quantity']
        closing_amount = df_filter.loc[index_val, 'closing_amount']

        total_quantity = quantity + issued_qty
        total_amount = price_x_qty + indent_item_amount

        closing_quantity = closing_quantity + issued_qty
        closing_amount = closing_amount + indent_item_amount

        df_inventory.loc[index_val, 'quantity'] = total_quantity
        df_inventory.loc[index_val, 'price_x_qty'] = total_amount
        df_inventory.loc[index_val, 'closing_quantity'] = closing_quantity
        df_inventory.loc[index_val, 'closing_amount'] = closing_amount

    return df_inventory


# ----------4 process wastages ----------------------------
def process_wastages(df_inventory, df_wastages):
    # branch	date	raw_material	unit	price	wastage_qty
    for i in range(0, len(df_wastages)):
        # print("-------- for loop ---------")
        branch = df_wastages.iloc[i]['branch']
        raw_material = df_wastages.iloc[i]['raw_material']
        wastage_qty = df_wastages.iloc[i]['wastage_qty']
        wast_item_amount = df_wastages.iloc[i]['amount']

        df_filter = df_inventory.loc[
                                 (df_inventory['branch'] == branch) &
                                 (df_inventory['raw_material'] == raw_material)
                                 ]
        # print('!!!! process_wastages- df_filter  \n', df_filter)
        if (len(df_filter) == 0):
            # print('item not found in inventory ===== ')
            del_items = branch, ' -- ', raw_material, ' -- ', wastage_qty, '-- ', wast_item_amount
            frappe.log_error("process_wastages", del_items)
            continue
        index_val = df_filter.index[0]
        quantity = df_filter.loc[index_val, 'quantity']
        price_x_qty = df_filter.loc[index_val, 'price_x_qty']
        closing_quantity = df_filter.loc[index_val, 'closing_quantity']
        closing_amount = df_filter.loc[index_val, 'closing_amount']

        total_quantity = quantity + wastage_qty
        total_amount = price_x_qty + wast_item_amount

        closing_quantity = closing_quantity + wastage_qty
        closing_amount = closing_amount + wast_item_amount

        df_inventory.loc[index_val, 'quantity'] = total_quantity
        df_inventory.loc[index_val, 'price_x_qty'] = total_amount
        df_inventory.loc[index_val, 'closing_quantity'] = closing_quantity
        df_inventory.loc[index_val, 'closing_amount'] = closing_amount

    return df_inventory


# -----------5 delete inventory summary of today data --------------
def delete_inventory_summary_of_specific_date(p_branch, p_date):
    sql = """
    DELETE FROM `tabInventory Summary` WHERE date = '{}'  AND branch = '{}'
    """
    # print(sql)
    sql = sql.format(p_date, p_branch)
    table = select_db_data(sql)
    return table


# ---------- 6 bulk insert inventory summary ------------------------
def bulk_insert_inventory_summary(df_inventory):
    # branch', 'date', 'raw_material', 'quantity', 'closing_quantity', 'price', 'unit', 'item'
    # branch, branch, user_name, `date`, raw_material, closing_quantity, price, unit, quantity
    # print('bulk_insert_ inventory_summary ')
    # print(df_inventory)
    for i in range(0, len(df_inventory)):
        # print("-------- for loop ---------")
        branch = df_inventory.iloc[i]['branch']
        date = df_inventory.iloc[i]['date']
        raw_material = df_inventory.iloc[i]['raw_material']
        quantity = df_inventory.iloc[i]['quantity']
        closing_quantity = df_inventory.iloc[i]['closing_quantity']
        price = df_inventory.iloc[i]['price']
        unit = df_inventory.iloc[i]['unit']
        price_x_qty = df_inventory.iloc[i]['price_x_qty']
        closing_amount = df_inventory.iloc[i]['closing_amount']
        doc = frappe.get_doc({
            'doctype': 'Inventory Summary',
            'branch': branch,
            'date': date,
            'raw_material': raw_material,
            'quantity': quantity,
            'closing_quantity': closing_quantity,
            'price': price,
            'unit': unit,
            'price_x_qty': price_x_qty,
            'closing_amount': closing_amount
        })
        doc.insert()


# ---------- 6.5 bulk insert inventory summary memory------------------------
def bulk_insert_inventory_summary_memory(df_inventory):
    # branch', 'date', 'raw_material', 'quantity', 'closing_quantity', 'price', 'unit', 'item'
    # branch, branch, user_name, `date`, raw_material, closing_quantity, price, unit, quantity
    # print('bulk_insert_ inventory_summary ')
    # print(df_inventory)
    for i in range(0, len(df_inventory)):
        # print("-------- for loop ---------")
        branch = df_inventory.iloc[i]['branch']
        date = df_inventory.iloc[i]['date']
        raw_material = df_inventory.iloc[i]['raw_material']
        quantity = df_inventory.iloc[i]['quantity']
        closing_quantity = df_inventory.iloc[i]['closing_quantity']
        price = df_inventory.iloc[i]['price']
        unit = df_inventory.iloc[i]['unit']
        price_x_qty = df_inventory.iloc[i]['price_x_qty']
        closing_amount = df_inventory.iloc[i]['closing_amount']
        doc = frappe.get_doc({
            'doctype': 'Inventory Summary',
            'branch': branch,
            'date': date,
            'raw_material': raw_material,
            'quantity': quantity,
            'closing_quantity': closing_quantity,
            'price': price,
            'unit': unit,
            'price_x_qty': price_x_qty,
            'closing_amount': closing_amount
        })
        doc.insert()


# -----------7 update raw material table closing stock -------------
def update_raw_material_table(df_inventory):
    # print('update raw material table closing stock')
    for i in range(0, len(df_inventory)):
        # print("-------- for loop ---------")
        raw_material = df_inventory.iloc[i]['raw_material']
        # quantity = df_inventory.iloc[i]['quantity']
        closing_quantity = df_inventory.iloc[i]['closing_quantity']
        closing_amount = df_inventory.iloc[i]['closing_amount']
        # print('  branch -', branch, '  date -', date, '  raw_material -',
        #       raw_material, '  quantity -', quantity, '  closing_quantity -',
        #       closing_quantity,  'price -', price, '  unit-', unit)
        frappe.db.set_value('Raw Material Only', raw_material,
                            'closing_stock', closing_quantity)
        frappe.db.set_value('Raw Material Only', raw_material,
                            'closing_amount', closing_amount)


#  --------------------SQL-----------------------
def get_raw_materials(p_branch):
    sql = """
    SELECT name as raw_material, branch as branch,
    date, item, unit, price, closing_stock, closing_amount
    FROM `tabRaw Material Only`
    WHERE branch = '{}'
    ORDER BY branch, raw_material
    """
    sql = sql.format(p_branch)
    table = select_db_data(sql)
    df_raw_materials = pd.DataFrame.from_records(table)
    return df_raw_materials


def get_stock_entry(p_branch, e_date):
    sql = """
    SELECT par.name AS par_name, chi.name AS chi_name,
    par.branch, chi.raw_material, chi.unit, chi.unit_price as price,
    chi.ord_qty, par.date, chi.amount, par.total_price
    FROM `tabStock Entry` par
    INNER JOIN `tabStock Entry Child` chi
    ON par.name = chi.parent
    WHERE date = '{}' AND branch = '{}'
    ORDER BY par.branch, chi.raw_material
    """
    sql = sql.format(e_date, p_branch)
    # print(sql)
    table = select_db_data(sql)
    df_stock_entry = pd.DataFrame.from_records(table)
    return df_stock_entry


def get_indents(p_branch, e_date):
    sql = """
    SELECT par.name, chi.name,
    par.branch, chi.raw_material, chi.req_qty,
    chi.issued_qty, par.date, chi.unit, chi.amount, par.total_price
    FROM `tabChef Indent By Dept` par
    INNER JOIN `tabChef Indent By Dept Child` chi
    ON par.name = chi.parent
    WHERE date = '{}' AND branch = '{}'
    ORDER BY par.branch, chi.raw_material
    """
    sql = sql.format(e_date, p_branch)
    table = select_db_data(sql)
    df_indnets = pd.DataFrame.from_records(table)
    return df_indnets


def get_wastages(p_branch, e_date):
    sql = """
    SELECT par.branch, par.date, chi.raw_material,
    chi.unit, chi.unit_price as price,  chi.wastage_qty,
    chi.amount, par.total_price
    FROM `tabInventory Wastage` par
    INNER JOIN `tabInventory Wastage Child` chi
    ON par.name = chi.parent
    WHERE date = '{}' and branch = '{}'
    ORDER BY par.branch, par.name, chi.name
    """
    sql = sql.format(e_date, p_branch)
    table = select_db_data(sql)
    df_wastages = pd.DataFrame.from_records(table)
    return df_wastages


def get_inv_sum_for_specific_date(p_branch, specific_date):
    sql = """
    SELECT branch, `date`, raw_material, unit, price, quantity,
    price_x_qty, closing_amount, closing_quantity
    FROM `tabInventory Summary`
    WHERE date = '{}' AND branch = '{}'
    UNION
    SELECT branch, '{}' as date, name as raw_material, unit, price, 0 as  quantity,
       0 as price_x_qty, 0 as closing_amount,  0 as closing_quantity
    FROM `tabRaw Material Only` rm
    WHERE branch = '{}' AND  rm.name NOT IN
    (
    SELECT raw_material
    FROM `tabInventory Summary`
    WHERE date = '{}' AND branch = '{}'
    )
    """
    sql = sql.format(specific_date, p_branch, specific_date, p_branch, specific_date, p_branch)
    # print(sql)
    table = select_db_data(sql)
    df_inv_summary_cur_date = pd.DataFrame.from_records(table)
    return df_inv_summary_cur_date


def select_db_data(sql):
    table = frappe.db.sql(sql, as_dict=True)
    return table


def create_inventory_summary_empty_data_frame():
    df = pd.DataFrame()
    columns_add = ['branch', 'date',
                   'raw_material', 'unit', 'price', 'quantity', 'price_x_qty',
                   'closing_quantity', 'closing_amount']
    for col in columns_add:
        df[col] = None
    return df


#  -------------------Utility--------------------
def collect_all_dates_until_today(input_date):
    current_date = datetime.today().date()
    date_list = []
    if (input_date > current_date):
        return date_list

    while input_date <= current_date:
        date_list.append(input_date)
        input_date += timedelta(days=1)

    return date_list


def collect_all_dates_between_from_and_to_date(from_date, to_date):
    date_list = []
    if (from_date > to_date):
        return date_list
    delta = to_date - from_date
    date_list = [from_date + timedelta(days=i) for i in range(delta.days + 1)]
    return date_list


def log_scheduler_job(start_status, end_statss, remarks):
    cur_date = datetime.now()
    doc = doc = frappe.new_doc('DevelopLog')
    doc.date = cur_date
    doc.source = 'scheduled_tasks - inventory_summary'
    doc.start = start_status
    doc.end = end_statss
    doc.remarks = remarks
    doc.save(ignore_permissions=True, ignore_version=True)


def get_today_date():
    current_date = datetime.today().date()
    return current_date


def get_previous_date(p_date):
    previous_date = p_date - timedelta(days=1)
    return previous_date


def get_stock_entry_for_60_days(p_branch, e_date):
    sql = """
    SELECT par.name AS par_name, chi.name AS chi_name,
    par.branch, chi.raw_material, chi.unit, chi.unit_price as price,
    chi.ord_qty, par.date, chi.amount, par.total_price
    FROM `tabStock Entry` par
    INNER JOIN `tabStock Entry Child` chi
    ON par.name = chi.parent
    WHERE date > '{}' AND branch = '{}'
    ORDER BY par.branch, chi.raw_material
    """
    sql = sql.format(e_date, p_branch)
    # print(sql)
    table = select_db_data(sql)
    df_stock_entry = pd.DataFrame.from_records(table)
    return df_stock_entry


def get_indents_for_60_days(p_branch, e_date):
    sql = """
    SELECT par.name  AS par_name, chi.name AS chi_name,
    par.branch, chi.raw_material, chi.req_qty,
    chi.issued_qty, par.date, chi.unit, chi.amount, par.total_price
    FROM `tabChef Indent By Dept` par
    INNER JOIN `tabChef Indent By Dept Child` chi
    ON par.name = chi.parent
    WHERE date > '{}' AND branch = '{}'
    ORDER BY par.branch, chi.raw_material
    """
    sql = sql.format(e_date, p_branch)
    # print(sql)
    table = select_db_data(sql)
    df_indnets = pd.DataFrame.from_records(table)
    return df_indnets


def get_wastages_for_60_days(p_branch, e_date):
    sql = """
    SELECT  par.name  AS par_name, chi.name AS chi_name,
    par.branch, par.date, chi.raw_material,
    chi.unit, chi.unit_price as price,  chi.wastage_qty,
    chi.amount, par.total_price
    FROM `tabInventory Wastage` par
    INNER JOIN `tabInventory Wastage Child` chi
    ON par.name = chi.parent
    WHERE date > '{}' and branch = '{}'
    ORDER BY par.branch, par.name, chi.name
    """
    sql = sql.format(e_date, p_branch)
    # print(sql)
    table = select_db_data(sql)
    df_wastages = pd.DataFrame.from_records(table)
    return df_wastages


def create_stock_entry_empty_data_frame():
    df = pd.DataFrame()
    columns_add = ['par_name', 'chi_name', 'branch',
                   'raw_material', 'unit', 'price', 'ord_qty', 'date',
                   'amount', 'total_price']
    for col in columns_add:
        df[col] = None
    return df


def create_indents_empty_data_frame():
    df = pd.DataFrame()
    columns_add = ['par_name', 'chi_name',
                   'branch', 'raw_material', 'req_qty',
                   'issued_qty', 'date', 'unit', 'amount', 'total_price']
    for col in columns_add:
        df[col] = None
    return df


def create_wastages_empty_data_frame():
    df = pd.DataFrame()
    columns_add = ['par_name', 'chi_name',
                   'branch', 'date', 'raw_material',
                   'unit', 'price',  'wastage_qty',
                   'amount', 'total_price']
    for col in columns_add:
        df[col] = None
    return df
