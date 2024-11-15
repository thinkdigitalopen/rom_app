frappe.ui.form.on("Development Work", {
	refresh(frm) {
		frm.add_custom_button('Run Scheduler', function(){

			// ------------------Inventory Counting---------------------------

			let api_url = "rom_app.scheduled_tasks.call_inventory_summary"
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
	//--------------------------------------------------------------------

	//--------------------------------------------------------------------
	frm.add_custom_button('Del Stock+ Data', function(){
	let api_url = "rom_app.clean_data.delete_stock_related_data"
		frappe.call({
			method: api_url,
			callback: function(res) {
				console.log(res);
			}
		});
    }, );
	//--------------------------------------------------------------------

	//--------------------------------------------------------------------
	// frm.add_custom_button('Reset Auto Incr', function(){
	// let api_url = "rom_app.clean_data.reset_auto_increment"
	// 	frappe.call({
	// 		method: api_url,
	// 		callback: function(res) {
	// 			console.log(res);
	// 		}
	// 	});
 //    }, );
	//--------------------------------------------------------------------


	},
});
