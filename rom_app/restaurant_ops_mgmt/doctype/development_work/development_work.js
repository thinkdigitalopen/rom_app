frappe.ui.form.on("Development Work", {
	refresh(frm) {
		frm.add_custom_button('Count Inventory', function(){

			// ------------------Inventory Counting---------------------------

			let api_url = "rom_app.scheduled_tasks.inventory_summary"
			frappe.call({
				method: api_url,
				callback: function(res) {
					console.log(res);
				}
			});

			// ------------------Inventory Counting---------------------------

    }, );


		//--------------------------------------------------------------------

			frm.add_custom_button('Read Config', function(){

			let api_url = "rom_app.scheduled_tasks.test_read_config"
			frappe.call({
				method: api_url,
				callback: function(res) {
					console.log(res);
				}
			});

    }, );

	},
});
