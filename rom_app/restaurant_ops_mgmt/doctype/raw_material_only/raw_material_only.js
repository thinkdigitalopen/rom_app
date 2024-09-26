frappe.ui.form.on("Raw Material Only", {
	refresh(frm) {

	},
	opening_stock : function(frm) {
		console.log('opening_stock');
		let opening_amount = frm.doc.price * frm.doc.opening_stock;
	    frm.set_value("opening_amount", opening_amount);
	},
	price : function(frm) {
		console.log('price');
		let opening_amount = frm.doc.price * frm.doc.opening_stock;
	    frm.set_value("opening_amount", opening_amount);
	},

});
