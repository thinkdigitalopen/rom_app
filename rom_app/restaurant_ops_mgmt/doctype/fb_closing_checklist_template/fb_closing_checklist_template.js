frappe.ui.form.on("FB Closing Checklist Template", {

	refresh(frm) {
		//frm.set_df_property('questions', 'cannot_add_rows', true);
        //frm.set_df_property('questions', 'cannot_delete_rows', true);
        //frm.set_df_property('questions', 'cannot_delete_all_rows', true);
		 //disable_drag_drop(frm);
	},

	onload(frm) {
		$('span.sidebar-toggle-btn').hide();
        $('.col-lg-2.layout-side-section').hide();
	}
});

function disable_drag_drop(frm) {
		frm.page.body.find('[data-fieldname="questions"] [data-idx] .data-row  .sortable-handle').removeClass('sortable-handle');

		   // frm.page.body.find('[data-fieldname="chef_close_questions"] [data-idx] .data-row').removeClass('sortable-handle');
	}
