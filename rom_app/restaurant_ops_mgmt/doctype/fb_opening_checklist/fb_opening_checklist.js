frappe.ui.form.on("FB Opening Checklist", {

	refresh(frm) {
		frm.set_df_property('questions', 'cannot_add_rows', true);
        frm.set_df_property('questions', 'cannot_delete_rows', true);
        frm.set_df_property('questions', 'cannot_delete_all_rows', true);
		console.log("refresh call");
		disable_drag_drop(frm);
	},

//=====================================================================
	onload(frm) {

		console.log("onload");
		$('span.sidebar-toggle-btn').hide();
        $('.col-lg-2.layout-side-section').hide();
		if (frm.is_new()) {
			console.log('is new - true')

			// let api_url = "rom_app.restaurant_ops_mgmt.api.get_the_branch_name_for_the_user"
			// let useremail = frappe.user.get_emails();
			// let email = useremail[0];


			//------------------------------------
			// frappe.call({
			// 	method: api_url,
			// 	args: {emailid: email},
			// 	callback: function(res) {
			// 		let branch__id = res.message.branch_id;
			// 		let branch__name = res.message.branch_name;
			// 		frm.set_value('branch_id', branch__id);
			// 		frm.set_value('branch_name', branch__name);
			// 		frm.set_df_property('branch_name', 'read_only', 1);
			// 		console.log('brnach id - '+ branch__id + ' = branch_name - ' + branch__name );
			let branch__id = frm.doc.branch;
			console.log('branch_id ____ ', branch__id);
					//-------------------------------------------------------
					frappe.call({
						method: 'rom_app.restaurant_ops_mgmt.api.get_fb_opening_checklist_child',
						args: {branch_param: branch__id},
						callback: function(res_questions) {
							frm.doc.questions = []
							$.each(res_questions.message, function(_i, e){
								console.log(_i);
								console.log(e);
								let item_question = e[2];
								let entry = frm.add_child("questions");
								entry.question = item_question;
							});
							refresh_field("questions");
							console.log("on load - 2nd frappe call end");
						}
					});
					//-------------------------------------------------------
			// 	}
			// });
			//------------------------------------

		};
		disable_drag_drop(frm);
	},
//=====================================================================


}

);
function disable_drag_drop(frm) {
		frm.page.body.find('[data-fieldname="questions"] [data-idx] .data-row .sortable-handle').removeClass('sortable-handle');

	}
