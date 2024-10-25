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

			let branch__id = frm.doc.branch;
			console.log('branch_id ____ ', branch__id);
					//-------------------------------------------------------
					frappe.call({
						method: 'rom_app.restaurant_ops_mgmt.api_checklist.get_fb_opening_checklist_child',
						args: {branch_param: branch__id},
						callback: function(res_questions) {
							frm.doc.questions = []
							$.each(res_questions.message, function(_i, e){
								console.log(_i);
								console.log(e);
								let question = e[2];
								let question_hid = e[3];
								let entry = frm.add_child("questions");
								entry.question = question;
								entry.question_hid = question_hid;
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
