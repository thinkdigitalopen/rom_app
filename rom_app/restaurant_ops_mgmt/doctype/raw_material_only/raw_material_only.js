frappe.ui.form.on("Raw Material Only", {
	refresh(frm) {


	},

	onload(frm)
	{
		// frappe.form.link_formatters['Branch'] = function(value, doc) {
		// 	console.log('link_formatters')
		// 	return "vaanth";
		// 	if(doc.branch_name) {
		// 		console.log('link_formatters-doc.branch_name ', doc.branch_name)
		// 		return "vaanth";
		// 		//return doc.branch_name;
		// 	}
		// 	console.log('link_formatters-value ', value)
		// 	return value;
		//  }

		$('span.sidebar-toggle-btn').hide();
        $('.col-lg-2.layout-side-section').hide();
/*
		if (frm.is_new()) {
			console.log('is_new');
			let useremail = frappe.user.get_emails();
			let email = useremail[0];
			console.log('email ',email);
			let api_url = "rom_app.restaurant_ops_mgmt.api.get_the_branch_name_for_the_user"
			//------------------------------------
			frappe.call({
			method: api_url,
			args: {emailid: email},
			callback: function(res) {
				console.log('res->',res);
				let branch__id = res.message.branch_id;
				let branch__name = res.message.branch_name;
				frm.set_value('branch', branch__id);


				frm.set_value('branch_name', branch__name);

				frappe.form.link_formatters['Branch'] = function(value, doc) {
					console.log('referwsh link_formatters')
					//return "vaanthref";
					if(doc.branch_name) {
						console.log('link_formatters-doc.branch_name ', doc.branch_name)
						return doc.branch_name;
					}
					console.log('link_formatters-value ', value)
					return value;
				}
			}
			});
		}*/




	},



});
