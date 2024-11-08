// Copyright (c) 2024, Pubs and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Responsible Person Template", {
// 	refresh(frm) {

// 	},
// });
frappe.listview_settings['Responsible Person Template'] = {
        refresh: function(listview) {
                $(".layout-side-section").hide();

        }
};
