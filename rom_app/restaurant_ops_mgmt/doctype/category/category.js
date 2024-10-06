
frappe.ui.form.on("Category", {
	onload(frm) {
        $('span.sidebar-toggle-btn').hide();
        $('.col-lg-2.layout-side-section').hide();
	},
	refresh(frm) {

	},
});
