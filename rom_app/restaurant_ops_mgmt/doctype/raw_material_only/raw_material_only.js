frappe.ui.form.on("Raw Material Only", {
	refresh(frm) {

	},

	onload(frm)
	{
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
				}
			});
		}

	},

	opening_stock : function(frm) {
		console.log('opening_stock');
		let opening_amount = frm.doc.price * frm.doc.opening_stock;
	    frm.set_value("opening_amount", opening_amount);
	},
	price : function(frm) {
		console.log('price');
		let opening_amount = frm.doc.price * frm.doc.opening_stock;
	    frm.set_value("opening_amount", opening_amount);
	},

});
