frappe.ui.form.on("Raw Material By Dept", {
	refresh(frm) {

	},
	onload(frm) {
        $('span.sidebar-toggle-btn').hide();
        $('.col-lg-2.layout-side-section').hide();
	},
});
