frappe.ui.form.on("Op Opening Checklist", {
   refresh(frm) {
		frm.set_df_property('questions', 'cannot_add_rows', true);
        frm.set_df_property('questions', 'cannot_delete_rows', true);
        frm.set_df_property('questions', 'cannot_delete_all_rows', true);
		disable_drag_drop(frm);
	},

	onload(frm) {
			disable_drag_drop(frm);
			$('span.sidebar-toggle-btn').hide();
        $('.col-lg-2.layout-side-section').hide();
		if (frm.is_new()) {
			// let useremail = frappe.user.get_emails();
			// let email = useremail[0];
			// let api_url = "rom_app.restaurant_ops_mgmt.api.get_the_branch_name_for_the_user";

			// frappe.call({
			// method: api_url,
			// args: {emailid: email},
			// callback: function(res) {
			 	let branch__id = frm.doc.branch;
			// 	let branch__name = res.message.branch_name;
			// 	frm.set_value('branch_id', branch__id);
			// 	frm.set_value('branch_name', branch__name);
			// 	frm.set_df_property('branch_name', 'read_only', 1);

				// -------------------------
				frappe.call({
				method: 'rom_app.restaurant_ops_mgmt.api.get_op_opening_checklist_child',
				args: {branch_param: branch__id},
				callback: function(res_questions) {
					frm.doc.questions = []

					$.each(res_questions.message, function(_i, e){
						console.log(_i, e);
						let entry = frm.add_child("questions");
						entry.area = e[2];
						entry.question = e[3];
					});
					refresh_field("questions");


					}
				});
				// -------------------------
/*
				}
			});*/
			// -------------------------
		};
		disable_drag_drop(frm);
    },


});

function disable_drag_drop(frm) {
		frm.page.body.find('[data-fieldname="questions"] [data-idx] .data-row .sortable-handle').removeClass('sortable-handle');
	}
