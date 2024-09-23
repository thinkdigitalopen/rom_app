frappe.ui.form.on("Dm Closing Checklist", {

	refresh(frm) {
		frm.set_df_property('dm_close_questions', 'cannot_add_rows', true);
        frm.set_df_property('dm_close_questions', 'cannot_delete_rows', true);
        frm.set_df_property('dm_close_questions', 'cannot_delete_all_rows', true);
		disable_drag_drop(frm);
	},

		onload(frm) {
		if (frm.is_new()) {

			let useremail = frappe.user.get_emails();
			let email = useremail[0];

			let api_url = "rom_app.restaurant_ops_mgmt.api.get_the_branch_name_for_the_user"

			//------------------------------------
			frappe.call({
			method: api_url,
			args: {emailid: email},
			callback: function(res) {
				let branch__id = res.message.branch_id;
				let branch__name = res.message.branch_name;
				frm.set_value('branch_id', branch__id);
				frm.set_value('branch_name', branch__name);
				frm.set_df_property('branch_name', 'read_only', 1);

				//-----------------------------

				frappe.call({
				method: "rom_app.restaurant_ops_mgmt.api.get_dm_closing_checklist_child",
				args: {branch_param: branch__id},
				callback: function(res_questions) {
					frm.doc.dm_close_questions = []

					$.each(res_questions.message, function(_i, e){
						let entry = frm.add_child("dm_close_questions");
						entry.dm_close_child_question = e[2];
					});
					refresh_field("dm_close_questions");


					}
				});

				}
			});
		};
		disable_drag_drop(frm);
    },

// ======================================================

});
function disable_drag_drop(frm) {
		frm.page.body.find('[data-fieldname="dm_close_questions"] [data-idx] .data-row  .sortable-handle').removeClass('sortable-handle');
	}

