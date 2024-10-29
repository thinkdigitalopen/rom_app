

frappe.ui.form.on("Ticket Report", {
	refresh(frm) {
		$('span.sidebar-toggle-btn').hide();
        $('.col-lg-2.layout-side-section').hide();

	},
	onload(frm) {
		$('span.sidebar-toggle-btn').hide();
        $('.col-lg-2.layout-side-section').hide();
	},
	validate(frm) {
		console.log('validate');
		let completed = frm.doc.completed;
		if(completed == true){
			console.log(' complete = true');
			result = find_user_is_from_the_dept(frm);
			if (result){
				console.log(' find user = true');
				return true;
			}
			else {
				console.log(' find user = false');
				frm.set_value('completed', false);
				warn_message(frm);
			}
		}
		else
		{
			console.log(' complete = false');
		}
	 }
});

function find_user_is_from_the_dept(frm){
	let useremail = frappe.user.get_emails();
	let department_id = frm.doc.department;

	let email = useremail[0];
	console.log('email ',email);
	let api_url = "rom_app.restaurant_ops_mgmt.api.check_the_user_has_the_selected_dept_role"
	let ret_value = false;
	frappe.call({
		method: api_url,
		args: {emailid: email, department_id:department_id},
		async:false,
		callback: function(res)
		{
			console.log('res', res);
			ret_value = res.message;
		}
	});
	console.log('finale return');
	return ret_value;
}

function warn_message(frm){
	let dis_msg = 'Only a user from the specified department can complete it!';
	let msg = frappe.msgprint({
					title: 'Warning',
					indicator: 'red',
					message: dis_msg,
					 primary_action:{
						'label': 'Close',
						action(values) {
							msg.hide();
						}
					}
				});

	throw dis_msg;
}
