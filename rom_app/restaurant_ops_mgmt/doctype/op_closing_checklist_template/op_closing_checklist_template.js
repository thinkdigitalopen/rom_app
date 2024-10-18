frappe.ui.form.on("Op Closing Checklist Template", {
	refresh(frm) {

	},
	onload(frm) {
        $('span.sidebar-toggle-btn').hide();
        $('.col-lg-2.layout-side-section').hide();
	},
});
