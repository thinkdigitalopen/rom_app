frappe.ui.form.on("Breakages Report", {
	refresh(frm) {

	},
	onload(frm) {
		$('span.sidebar-toggle-btn').hide();
        $('.col-lg-2.layout-side-section').hide();

		// if (frm.is_new()) {
			// console.log('is_new');
			// let useremail = frappe.user.get_emails();
			// let email = useremail[0];
			// console.log('email ',email);
			// let api_url = "rom_app.restaurant_ops_mgmt.api.get_the_branch_name_for_the_user"
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
			// 	asset_master_set_query(frm, branch__id,  doc.name);
					// //-----------------------------
					// console.log("getting user role ");
					// let systemmanager_user_role_avail = frappe.user.has_role("System Manager");
					// let chef_user_role_avail = frappe.user.has_role("Rom_Chef_Role");
					// let dm_user_role_avail = frappe.user.has_role("Rom_DM_Role");
     //
					// let allroles = frappe.user_roles;
					// console.log('allroles-- > ', allroles);
     //
					// console.log('systemmanager_user_role_avail - ',systemmanager_user_role_avail);
					// console.log('chef_user_role_avail - ',chef_user_role_avail);
					// console.log('dm_user_role_avail - ',dm_user_role_avail);
					// let category_param = 0;
     //
					// if (chef_user_role_avail){
					// 	frappe.db.get_doc('Category', null,
					// 					  {  branch: branch__id,
					// 						  category_type : 'Kitchen' })
					// 	.then(doc => {
					// 		frm.set_value('category_name', doc.category_name);
					// 		frm.set_value('category_id', doc.name);
					 		// asset_master_set_query(frm, branch__id,  doc.name);
					// 	})
					// }
					// else if (dm_user_role_avail){
					// 	frappe.db.get_doc('Category', null,
					// 					  {  branch: branch__id,
					// 						  category_type : 'Dining' })
					// 	.then(doc => {
					// 		frm.set_value('category_name', doc.category_name);
					// 		frm.set_value('category_id', doc.name);
					// 		 asset_master_set_query(frm, branch__id, doc.name);
					// 	})
					// }
		// 		}
		// 	});
		// }else{
  //           // let branch__id = frm.doc.branch_id;
		// 	// let category_id = frm.doc.category_id;
		// 	// asset_master_set_query(frm, branch__id);
		// }
    },

	item: function(frm) {
		console.log(' item selected ');
		calculate_total_breakage_cost(frm);
	},

	quantity: function(frm) {
		calculate_total_breakage_cost(frm);
	},

});

// function asset_master_set_query(frm, branch__id ) {
//
// 	frm.set_query("item", function(){
// 						return {
// 							"filters": [
// 								["Asset Master", "branch_id", "=", branch__id],
//
// 							]
// 						}
// 				    });
// }

function calculate_total_breakage_cost(frm) {
	let item_price = frm.doc.item_price;
	let quantity = frm.doc.quantity;
	if(item_price && quantity){
		let total_cost = item_price * quantity;
		console.log('total_cost=',total_cost);
		frm.set_value('cost', total_cost);
	}
}


