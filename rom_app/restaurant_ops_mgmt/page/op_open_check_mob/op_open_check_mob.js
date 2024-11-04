frappe.pages['op-open-check-mob'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Op Opn Chk',
		single_column: true
	});

	load_the_first_screen();
	page.set_primary_action('Save', () => save_form());
	page.set_secondary_action('Refresh', () => refresh_form());

	function save_form(){
		console.log(' save_form ');

		let values = page.get_form_values();
		console.log(typeof values);
		object_length = Object.keys(values).length;
		console.log('object_length - ',object_length);
		if (object_length == 0){
			return;
		}

		let api_url = "rom_app.restaurant_ops_mgmt.api_mobile_opo.update_op_opening_checklist_child_mobile"

		frappe.call({
			method: api_url,
			args: {form_values: values},
			callback: function(res) {
				console.log(res);

				let msg = frappe.msgprint({
					title: 'Info',
					indicator: 'green',
					message: 'Document updated successfully',
					 primary_action:{
						'label': 'Close',
						action(values) {
							console.log(values);
							msg.hide();
						}
					}
				});
			}
		});
	}

	function refresh_form(){
		window.location.reload(true);
	}

	function load_the_first_screen() {
		let email = get_user_email();
		let basic_user_details = get_the_basic_user_details(email);
		console.log("basic_user_details ***** ", basic_user_details);
		build_action_button_ui_for_seven_dates(basic_user_details);
	}

	function get_user_email(){
		let useremail = frappe.user.get_emails();
		let email = useremail[0];
		console.log('email -> ', email);
		return email;
	}

	function get_the_basic_user_details(email) {
		let api_url = "rom_app.restaurant_ops_mgmt.api.get_the_branch_for_the_user_based_on_email_id";

		let branch;
		let current_date;
		let seven_dates;

		frappe.call({
			method: api_url,
			args: {emailid: email},
			async: false,
			callback: function(res) {
				branch = res.message.branch;
				current_date = res.message.current_date;
				seven_dates =  res.message.seven_dates;
			}
		});

		let user_name = frappe.session.user_fullname;

		let basic_user_details = {
			branch: branch,
			current_date: current_date,
			email_id: email,
			user_name: user_name,
			seven_dates: seven_dates
		}
		return basic_user_details;
	}

	function build_action_button_ui_for_seven_dates(basic_user_details){
		basic_user_details.seven_dates.forEach(function (item, index) {
			console.log('item', item);
			page.add_action_item(item, () => load_items_for_the_date(item, basic_user_details));
		});
		let html_text =  "<h5>Pick the date from the top menu</h5> "
		page.add_field({
			options: html_text,
			fieldtype: 'HTML',
			fieldname: 'html_field',
		});
	}

	function load_items_for_the_date(load_date, basic_user_details) {
		console.log('load_items_for_the_date');
		console.log('load_date ', load_date);
		basic_user_details.load_date = load_date;
		console.log('basic_user_details ', basic_user_details);
		// page.set_title(load_date)
		console.log(' %%%%%%%%%%%% clear fields %%%%%%%%%%%% ');
		page.clear_fields();
		basic_user_details = get_op_opening_checklist_child(load_date, basic_user_details);
		let areas = get_distict_area_for_branch(basic_user_details);
		console.log(areas);
		build_home_ui_for_area(areas, basic_user_details);
	}

	function get_op_opening_checklist_child(load_date, basic_user_details) {
		console.log(" $$$$$$$$$ ");
		console.log(" load_date ", load_date);

		rec_result = find_out_if_the_record_exist(load_date, basic_user_details);
		console.log("parent_name ***** ", rec_result);
		console.log("basic_user_details ***** ", basic_user_details);
		//add parent_name to the basic_user_details
		basic_user_details.parent_name = rec_result.parent_name;
		basic_user_details.load_date = load_date;
		console.log('basic_user_details-parent-name ', basic_user_details);
		// get_op_opening_checklist_child_mobile(basic_user_details);
		return basic_user_details;
	 }

	function find_out_if_the_record_exist(load_date, user_details) {
		let api_url = "rom_app.restaurant_ops_mgmt.api_mobile_opo.op_opening_check_record_exits_otherwise_create_one";
		let ret_message = {};
		frappe.call({
			method: api_url,
			args: {
				branch: user_details.branch,
				current_date: user_details.current_date,
				email_id: user_details.email_id,
				user_name: user_details.user_name,
				load_date: load_date
			},
			async: false,
			callback: function(res) {
				console.log("find_out_if_the_record_exist--->", res);
				ret_message = res.message;
			}
		});
		return ret_message;
	}

	function build_read_only_fields_on_ui(basic_user_details){

		let branch_lable = "Branch : " + basic_user_details.branch;
		page.add_field({
					default: branch_lable,
					fieldtype: 'Data',
					fieldname: 'field_branch',
					read_only: 1
				});

		let user_label = "User : " + basic_user_details.user_name;
		page.add_field({
					default: user_label,
					fieldtype: 'Data',
					fieldname: 'field_user',
					read_only: 1
				});

		let current_date_lable = "Date : " + basic_user_details.load_date;
		page.add_field({
					default: current_date_lable,
					fieldtype: 'Data',
					fieldname: 'field_current_date',
					read_only: 1,
				});

		let parent_id_lable = "Parent Id : " + basic_user_details.parent_name;
			page.add_field({
						default: parent_id_lable,
						fieldtype: 'Data',
						fieldname: 'field_parent_name',
						read_only: 1,
						hidden: 1
			});
	}

	function get_distict_area_for_branch(user_details) {
		console.log('get_distict_area_for_branch', user_details);
		let areas = {};
		let api_url = "rom_app.restaurant_ops_mgmt.api_mobile_opo.get_distinct_area_for_branch";

		frappe.call({
			method: api_url,
			args: {
				branch_param: user_details.branch,
			},
			async: false,
			callback: function(res) {
				console.log("find_out_area_exist--->", res);
				areas = res.message;
				console.log("areas --->", areas);
			}
		});

		let areas_arr = convert_area_to_array(areas);
		return areas_arr;
	}




	function build_home_ui_for_area(areas, basic_user_details) {
		console.log("~~build_home_ui_for_area", areas);
		console.log("basic_user_details", basic_user_details);

		areas.forEach(function (item, index) {
			console.log('item', item);
			page.add_inner_button(item, () => load_items_for_the_area(item, basic_user_details));
			//page.add_inner_button(item , () => load_items_for_the_area(item, basic_user_details));
		});

		let html_text =  "<h5>Pick the area from the top menu</h5> "
		page.add_field({
			options: html_text,
			fieldtype: 'HTML',
			fieldname: 'html_field',
		});
	}

	function load_items_for_the_area(area, basic_user_details) {
		console.log('load_items_for_the_area');
		console.log('area', area);
		console.log('basic_user_details', basic_user_details);
		page.set_title(area)
		console.log(area);
		page.clear_fields();
		let items_based_on_area = get_items_based_on_the_area(area, basic_user_details);
		build_read_only_fields_on_ui(basic_user_details);
		build_check_fields_on_ui(items_based_on_area);
	}








	function build_check_fields_on_ui(items_based_on_area){
		console.log("start - build_check_fields_on_ui");
		// 'parent_name': 4,
		// 'date': datetime.date(2024, 10, 14),
		// 'user_name': 'op1',
		// 'branch': '9',
		// 'child_name': 7,
		// 'audit': 1,
		// // 'question': 'Date Sticker Checked'
		$.each(items_based_on_area, function(_i, e){
			let child_name = e.child_name;
			let child_question = e.question;
			let child_audit = e.audit;
			let child_area = e.area;
			let disp_text =  child_name +" = "+ child_question +" = "+ child_audit + " <> " +child_area;
			console.log(disp_text);

			let field_check = page.add_field({
				label: child_question,
				fieldtype: 'Check',
				fieldname: child_name,
				default: child_audit
			});
		});
		console.log("()()()()()()");
	}

	function get_items_based_on_the_area(area, basic_user_details) {
		let items_based_on_area = [];
		let api_url = "rom_app.restaurant_ops_mgmt.api_mobile_opo.get_op_opening_checklist_child_mobile_area";
		console.log('basic_user_details', basic_user_details);
		console.log('area', area);
		frappe.call({
			method: api_url,
			args: {
				branch_param: basic_user_details.branch,
				area_param: area,
				load_date:  basic_user_details.load_date,
			},
			async: false,
			callback: function(res) {
				items_based_on_area = res.message;
				console.log("res --->", res);
				console.log("items_bsed_on_area --->", items_based_on_area);
			}
		});
		return items_based_on_area;
	}

	function convert_area_to_array(areas){
		let areas_array = [];

		areas.forEach(function (item, index) {
			console.log(item, index);
			console.log(item.area);
			areas_array.push(item.area);
		})
		return areas_array;
	};
}

