frappe.listview_settings['Inventory Summary'] = {
	onload: function(listview) {
		let branch_filter = 0;
		console.log('list view');
		let useremail = frappe.user.get_emails();
		let email = useremail[0];
		let api_url = "rom_app.restaurant_ops_mgmt.api.get_the_branch_name_for_the_user"
		//------------------------------------
		frappe.call({
			method: api_url,
			args: {emailid: email},
			async: false,
				callback: function(res) {
					console.log('inside call ');
					branch_filter = res.message.branch_id;
					console.log('inside call branch_filter ', branch_filter);
				}
		});
		//------------------------------------
		console.log('outside callback - branch_filter --> ', branch_filter);
		frappe.route_options = { "branch_id": branch_filter };
		listview.refresh();

	}
}


