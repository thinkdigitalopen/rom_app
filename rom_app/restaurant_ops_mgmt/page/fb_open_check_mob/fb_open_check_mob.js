frappe.pages['fb-open-check-mob'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'FB Opn',
		single_column: true
	});

	page.set_primary_action('Save', () => save_form());
	page.set_secondary_action('Refresh', () => refresh_form());

	function save_form(){
		console.log(' save_form ');
		let values = page.get_form_values();
		console.log(values);
		let api_url = "rom_app.restaurant_ops_mgmt.api_mobile_fbo.update_fb_opening_checklist_child_mobile"

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

	get_fb_opening_checklist_child();


	function get_fb_opening_checklist_child() {
		// window.location.reload(true);
		let email = get_user_email();
		let basic_user_details = get_the_basic_user_details(email);
		console.log("basic_user_details ***** ", basic_user_details);

		parent_name = find_out_if_the_record_exist(basic_user_details);

		console.log("parent_name ***** ", parent_name);
		console.log("basic_user_details ***** ", basic_user_details);
		basic_user_details = add_parent_name_to_the_basic_user_details(basic_user_details, parent_name);
		console.log('basic_user_details-parent-name ', basic_user_details);
		build_read_only_fields_on_ui(basic_user_details);
		get_fb_opening_checklist_child_mobile(basic_user_details);
	 }

	function add_parent_name_to_the_basic_user_details(basic_user_details, parent_name){
		 basic_user_details.parent_name = parent_name;
		 return basic_user_details;
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

		frappe.call({
			method: api_url,
			args: {emailid: email},
			async: false,
			callback: function(res) {
				branch = res.message.branch;
				current_date = res.message.current_date;
			}
		});

		let user_name = frappe.session.user_fullname;

		let basic_user_details = {
			branch: branch,
			current_date: current_date,
			email_id: email,
			user_name: user_name,
		}
		console.log(basic_user_details);
		return basic_user_details;
	}

	function find_out_if_the_record_exist(user_details) {
		let api_url = "rom_app.restaurant_ops_mgmt.api_mobile_fbo.fb_opening_check_today_record_exits_otherwise_create_one";
		let parent_name = 0;
		frappe.call({
			method: api_url,
			args: {
				branch: user_details.branch,
				current_date: user_details.current_date,
				email_id: user_details.email_id,
				user_name: user_details.user_name
			},
			async: false,
			callback: function(res) {
				console.log("find_out_if_the_record_exist--->", res);
				parent_name = res.message;
			}
		});
		return parent_name;
	}

	function get_fb_opening_checklist_child_mobile(basic_user_details){
		console.log("start - get_fb_opening_checklist_child_mobile");
		console.log("start - basic_user_details", basic_user_details);

		// 'parent_name': 4,
		// 'date': datetime.date(2024, 10, 14),
		// 'user_name': 'fb1',
		// 'branch': '9',
		// 'child_name': 7,
		// 'audit': 1,
		// 'question': 'Date Sticker Checked'
		let api_url = 'rom_app.restaurant_ops_mgmt.api_mobile_fbo.get_fb_opening_checklist_child_mobile';

		frappe.call({
			method:api_url,
			args: {branch_param: basic_user_details.branch},
			async:false,
			callback: function(res_questions) {
				$.each(res_questions.message, function(_i, e){
					let child_name = e.child_name;
					let child_question = e.question;
					let child_audit = e.audit;
					let disp_text =  child_name +" = "+ child_question +" = "+ child_audit;
					console.log(disp_text);

					let field_check = page.add_field({
						label: child_question,
						fieldtype: 'Check',
						fieldname: child_name,
						default: child_audit
					});
				});
				console.log("frappe callback end - get_fb_opening_checklist_child_mobile");
			}
		});
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

		let current_date_lable = "Date : " + basic_user_details.current_date;
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
}

