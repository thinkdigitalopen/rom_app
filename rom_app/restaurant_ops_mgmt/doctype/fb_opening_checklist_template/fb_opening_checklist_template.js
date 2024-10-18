frappe.ui.form.on("FB Opening Checklist Template", {
	onload(frm) {
        $('span.sidebar-toggle-btn').hide();
        $('.col-lg-2.layout-side-section').hide();
		// disable_drag_drop(frm);
	},
	refresh(frm) {
		// disable_drag_drop(frm);
	},
});
function disable_drag_drop(frm) {
		frm.page.body.find('[data-fieldname="questions"] [data-idx] .data-row  .sortable-handle').removeClass('sortable-handle');
	}
