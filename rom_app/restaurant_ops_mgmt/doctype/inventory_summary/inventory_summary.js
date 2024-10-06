
frappe.ui.form.on("Inventory Summary", {
	refresh(frm) {


	},
	onload(frm) {
        $('span.sidebar-toggle-btn').hide();
        $('.col-lg-2.layout-side-section').hide();
	},

});
