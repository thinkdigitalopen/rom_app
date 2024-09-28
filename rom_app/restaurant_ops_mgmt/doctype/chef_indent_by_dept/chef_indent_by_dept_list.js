frappe.listview_settings['Chef Indent By Dept'] = {
	onload: function(listview) {
		let branch_filter = '';
		console.log('list view');
		let useremail = frappe.user.get_emails();
		let email = useremail[0];
		let api_url = "rom_app.restaurant_ops_mgmt.api.get_the_branch_name_for_the_user"

		//console.log("getting user role ");
		let systemmanager_user_role_avail = frappe.user.has_role("System Manager");
		//let chef_user_role_avail = frappe.user.has_role("Rom_Chef_Role");
		let store_user_role_avail = frappe.user.has_role("Rom_Store_Role");
		//console.log('store_user_role_avail - ',store_user_role_avail);
		//let dm_user_role_avail = frappe.user.has_role("Rom_STORE_Role");

		//let allroles = frappe.user_roles;
//		console.log('allroles-- > ', allroles);

		//console.log('chef_user_role_avail - ',chef_user_role_avail);


		if (store_user_role_avail){
			//------------------------------------
			frappe.call({
				method: api_url,
				args: {emailid: email},
				async: false,
					callback: function(res) {
						console.log('inside call ');
						branch_filter = res.message.branch_name;

						console.log('inside call branch_filter ', branch_filter);
					}
			});
			//------------------------------------
			console.log('outside callback - branch_filter --> ', branch_filter);
			frappe.route_options = { "branch_name": ["like", "%" + branch_filter + "%"] };
			listview.refresh();
		}
	}
}

//branch_name=["like"%2C"%25Heavens+Park%25"]
// {“field”:[“not like”, “%” + frm.doc.name + “%”]}
