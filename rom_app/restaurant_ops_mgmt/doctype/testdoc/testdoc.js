frappe.ui.form.on("TestDoc", {
	refresh(frm) {

	},
});
// frappe.ui.form.on("TestDocChild",{
// 	assign: function(frm, cdt, cdn){
// 		var d = locals[cdt][cdn];
// 		frappe.msgprint('button clicked');
// 	}
// })


frappe.ui.form.on("TestDocChild", {
	onload: function (frm, cdt, cdn) {
		console.log('child  0');
	let btn = document.createElement('a');
	btn.innerText = 'Refresh';
	btn.className = 'grid-upload btn btn-xs btn-default';
	frm.fields_dict.child_table.grid.wrapper.find('.grid-upload').removeClass('hide').parent().append(btn);
	btn.addEventListener("click", function(){
		frappe.msgprint('button clicked');
	});
	}
})
