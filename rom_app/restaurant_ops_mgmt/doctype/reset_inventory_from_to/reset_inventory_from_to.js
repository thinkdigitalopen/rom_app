frappe.ui.form.on("Reset Inventory From To", {
	refresh(frm) {

		frm.add_custom_button('Reset Inv. Summary From To', function(){

				let branch = frm.doc.branch;
				let from_date = frm.doc.from_date;
				let to_date = frm.doc.to_date;

				if(!branch) {
					alert('branch is empty');
					return;
				}

				if(!from_date) {
					alert('from date is empty');
					return;
				}

				if(!to_date) {
					alert('to date is empty');
					return;
				}

				console.log('branch ',branch);
				console.log('from_date ',from_date);
				console.log('to_date ',to_date);

				let api_url = "rom_app.scheduled_tasks.inventory_summary_for_start_and_end_date_enquee"
                // let api_url = "rom_app.scheduled_tasks.inventory_summary_for_start_and_end_date"

				frappe.call(
					{
						method: api_url,
						args:
						{
							p_branch: branch,
							p_date: from_date,
							p_end_date: to_date
						},
						async:false,
						freeze:true,
						freeze_message: "Processing",
						callback: function(res)
						{
							console.log(res.message);
						}
					},);

		});


    // scheduler job - for testing
	frm.add_custom_button('Job - 60 days BEFORE Reset Inv. Summary ', function(){
				let api_url = "rom_app.scheduled_tasks.call_inventory_summary_morning_60_days_before"
				frappe.call(
					{
						method: api_url,
						args:
						{
						},
						async:false,
						freeze:true,
						freeze_message: "Processing",
						callback: function(res)
						{
							console.log(res.message);
						}
					},);
		});



	frm.add_custom_button('Job - Fast Update Morning', function(){
				let api_url = "rom_app.scheduled_tasks.call_inventory_summary_morning_for_today_with_one_time_db_write"
				frappe.call(
					{
						method: api_url,
						args:
						{
						},
						async:false,
						freeze:true,
						freeze_message: "Processing",
						callback: function(res)
						{
							console.log(res.message);
						}
					},);
		});


	},
});
