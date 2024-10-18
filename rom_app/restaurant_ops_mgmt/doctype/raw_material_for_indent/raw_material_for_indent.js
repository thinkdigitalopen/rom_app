frappe.ui.form.on("Raw Material For Indent", "onload", function(frm) {

	$('span.sidebar-toggle-btn').hide();
    $('.col-lg-2.layout-side-section').hide();


	// frm.fields_dict["items"].grid.get_field("raw_material").get_query = function(doc) {
	// 	return {
	// 		filters: {
	// 		'branch': frm.doc.branch,
	// 		}
	// 	}
	// };
 //
 //
	// frm.set_query("department", function() {
	// 	return {
	// 		"filters": {
	// 			"branch": frm.doc.branch,
	// 		}
	// 	};
	// });


});
