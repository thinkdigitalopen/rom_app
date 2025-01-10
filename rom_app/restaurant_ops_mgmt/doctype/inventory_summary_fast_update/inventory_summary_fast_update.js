frappe.ui.form.on("Inventory Summary Fast Update", {
	refresh(frm) {

frm.add_custom_button('Update Inventory Summary for Today ', function(){
				let branch = frm.doc.branch;
				let end_date = frm.doc.update_date;
				if(!branch) {
					alert('branch is empty');
					return;
				}

				if(!end_date) {
					alert('update date is empty');
					return;
				}

				console.log('branch ',branch);
				console.log('update date ',end_date);

				let api_url = "rom_app.scheduled_tasks.inventory_summary_one_time_db_write"
				frappe.call(
					{
						method: api_url,
						args:
						{
							p_branch: branch,
							p_date: end_date
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


frm.add_custom_button('Job ', function(){
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
