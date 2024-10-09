frappe.ui.form.on("Stock Entry Template Type", {
	refresh(frm) {

	},
	onload(frm)
	{
        $('span.sidebar-toggle-btn').hide();
        $('.col-lg-2.layout-side-section').hide();
	}
});
