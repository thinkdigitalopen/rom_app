frappe.ui.form.on("FB Closing Checklist", {

	refresh(frm) {
		frm.set_df_property('questions', 'cannot_add_rows', true);
        frm.set_df_property('questions', 'cannot_delete_rows', true);
        frm.set_df_property('questions', 'cannot_delete_all_rows', true);
		disable_drag_drop(frm);
	},

	onload(frm) {
		$('span.sidebar-toggle-btn').hide();
        $('.col-lg-2.layout-side-section').hide();

		if (frm.is_new()) {

				let branch__id = frm.doc.branch;
				console.log('branch__id-> ',branch__id);

					// -----------------------------
				let api_url_child = "rom_app.restaurant_ops_mgmt.api.get_fb_closing_checklist_child"
				frappe.call({
				method: api_url_child,
				args: {branch_param: branch__id},
				callback: function(res_questions) {
					frm.doc.questions = []

					$.each(res_questions.message, function(_i, e){
						let entry = frm.add_child("questions");
						entry.question = e[2];
					});

					refresh_field("questions");

				}
				});
				// -----------------------------

		};
		disable_drag_drop(frm);
    },
 // ======================================================

});
function disable_drag_drop(frm) {
		frm.page.body.find('[data-fieldname="questions"] [data-idx] .data-row  .sortable-handle').removeClass('sortable-handle');
	}

