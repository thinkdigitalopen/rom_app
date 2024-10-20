frappe.ui.form.on("Stock Entry Template", {
	refresh(frm) {

	},
	onload(frm) {
		 $('span.sidebar-toggle-btn').hide();
        $('.col-lg-2.layout-side-section').hide();

		if (frm.is_new()) {

			console.log('is_new');

			// let useremail = frappe.user.get_emails();
			// let email = useremail[0];
			// //console.log('email ',email);
			// let api_url = "rom_app.restaurant_ops_mgmt.api.get_the_branch_name_for_the_user"
   //
			// //------------------------------------
			// frappe.call({
			// method: api_url,
			// args: {emailid: email},
			// callback: function(res) {
			// 	let branch__id = res.message.branch_id;
			// 	let branch__name = res.message.branch_name;
			// 	frm.set_value('branch_id', branch__id);
			// 	frm.set_value('branch_name', branch__name);
			// 	frm.set_df_property('branch_name', 'read_only', 1);
			// 	console.log('branch_id-', branch__id, '=== branch_name-', branch__name);
   //
			// 	frm.set_query("stock_entry_template", function() {
			// 		return {
			// 			"filters": {
			// 				"branch": branch__id
			// 			}
			// 		};
			// 	});
   //
			// 	frm.fields_dict["raw_material_list"].grid.get_field("raw_material").get_query = function(doc) {
			// 		return {
			// 			filters: {
			// 				'branch': frm.doc.branch_id,
			// 			}
			// 		}
			// 	};
   //
	 	// 	}
	 	// 	});

			//------------------------------------

	 	}
	 // 	else{
  //
		// 	 //    let branch__id =  frm.doc.branch_id;
		// 		// frm.set_query("stock_entry_template", function() {
		// 		// 	return {
		// 		// 		"filters": {
		// 		// 			"branch": branch__id
		// 		// 		}
		// 		// 	};
		// 		// });
  //   //
		// 		// frm.fields_dict["raw_material_list"].grid.get_field("raw_material").get_query = function(doc) {
		// 		// 	return {
		// 		// 		filters: {
		// 		// 			'branch': branch__id,
		// 		// 		}
		// 		// 	}
		// 		// };
  //
		// }
	 }
});



