frappe.ui.form.on("Raw Material For Indent", "onload", function(frm) {
	frm.fields_dict["items"].grid.get_field("raw_material").get_query = function(doc) {
		return {
			filters: {
			'branch': frm.doc.branch,
			}
		}
	}
});
