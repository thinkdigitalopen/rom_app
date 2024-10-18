// Copyright (c) 2024, Pubs and contributors
// For license information, please see license.txt

frappe.ui.form.on("Raw Material Group", {
	onload(frm) {
        $('span.sidebar-toggle-btn').hide();
        $('.col-lg-2.layout-side-section').hide();
	},
	refresh(frm) {

	},
});
