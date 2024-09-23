frappe.ui.form.on("Chef Production", {
	refresh(frm) {
		frm.set_df_property('briyani_category_list', 'cannot_add_rows', true);
        frm.set_df_property('briyani_category_list', 'cannot_delete_rows', true);
        frm.set_df_property('briyani_category_list', 'cannot_delete_all_rows', true);

		frm.set_df_property('chicken_category_list', 'cannot_add_rows', true);
        frm.set_df_property('chicken_category_list', 'cannot_delete_rows', true);
        frm.set_df_property('chicken_category_list', 'cannot_delete_all_rows', true);
		console.log("refresh call");
		disable_drag_drop_briyani_category_list(frm);
		disable_drag_drop_chicken_category_list(frm);
	},
	onload(frm) {
		if (frm.is_new()) {

			console.log('is_new');

			let useremail = frappe.user.get_emails();
			let email = useremail[0];
			//console.log('email ',email);
			let api_url = "rom_app.restaurant_ops_mgmt.api.get_the_branch_name_for_the_user"

			//------------------------------------
			frappe.call({
			method: api_url,
			args: {emailid: email},
			callback: function(res) {
				let branch__id = res.message.branch_id;
				let branch__name = res.message.branch_name;
				frm.set_value('branch_id', branch__id);
				frm.set_value('branch_name', branch__name);
				frm.set_df_property('branch_name', 'read_only', 1);
				//console.log('branch_id-', branch__id, '=== branch_name-', branch__name);

				//-----------------------------

				frappe.call({
				method: "rom_app.restaurant_ops_mgmt.api.get_chef_production_checklist_child_briyani",
				args: {branch_param: branch__id},
				callback: function(res_questions) {
					frm.doc.briyani_category = []
					console.log('briyani_category_list');
					console.log(res_questions);
					$.each(res_questions.message, function(_i, e){
						//console.log('_i',_i);
						//console.log('e',e);
						let briyani_category = e[2];
						let portion = e[3];
						let rateportion = e[4];
						console.log(briyani_category,portion, rateportion);

						let entry = frm.add_child("briyani_category_list");
						entry.briyani_category = briyani_category;
						entry.portion = portion;
						entry.rateportion = rateportion;
					});
					refresh_field("briyani_category_list");
					}
				});
				//console.log('*************************');
			//-----------------------------
				frappe.call({
				method: "rom_app.restaurant_ops_mgmt.api.get_chef_production_checklist_child_chicken",
				args: {branch_param: branch__id},
				callback: function(res_questions) {
					//console.log('chicken_category_list');
					//console.log(res_questions);
					frm.doc.chicken_category = []

					$.each(res_questions.message, function(_i, e){
						//console.log(_i,e);
						let chicken_category = e[2];
						let uom = e[3];
						let rate = e[4];
						console.log(chicken_category,uom, rate);
						let entry = frm.add_child("chicken_category_list");
						entry.chicken_category = chicken_category;
						entry.uom = uom;
						entry.rate = rate;
					});
					refresh_field("chicken_category_list");
					}
				});
				//console.log('*************************');

			//-----------------------------

				}
			});


		};
		disable_drag_drop_briyani_category_list(frm);
		disable_drag_drop_chicken_category_list(frm);
    },
});



frappe.ui.form.on("Chef Prod Child Briyani", {
    balance_portion:function(frm,cdt,cdn) {
		var d = locals[cdt][cdn];

		let balance_portion_temp = 0;
		let rateportion_temp = 0;
		let cal_val = 0;

		if(parseInt(d.balance_portion)>=0)
			balance_portion_temp = d.balance_portion;

		if(parseInt(d.rateportion)>=0)
			rateportion_temp = d.rateportion;

		cal_val = balance_portion_temp * rateportion_temp;

		console.log('balance_portion_temp->', balance_portion_temp);
		console.log('rateportion_temp->',rateportion_temp);
		console.log('cal_val->', cal_val);

		frappe.model.set_value(cdt, cdn, 'wastage_amount', cal_val);

		console.log('locals->', locals);
		console.log('cdt->', cdt);
		console.log('cdn->', cdn);
		console.log('d->', d);

		// briyani category wastage amount total
		console.log('briyani category wastage amount total');
		var waste_total = 0;
		frm.doc.briyani_category_list.forEach(function(d) { waste_total += d.wastage_amount; });
		console.log('waste_total', waste_total);
		frm.set_value("briyani_category_wastage_amount", waste_total);
		refresh_field("briyani_category_wastage_amount");

    }
});

frappe.ui.form.on("Chef Prod Child Briyani", {
    rateportion:function(frm,cdt,cdn) {
		var d = locals[cdt][cdn];

		let balance_portion_temp = 0;
		let rateportion_temp = 0;
		let cal_val = 0;

		if(parseInt(d.balance_portion)>=0)
			balance_portion_temp = d.balance_portion;

		if(parseInt(d.rateportion)>=0)
			rateportion_temp = d.rateportion;

		cal_val = balance_portion_temp * rateportion_temp;

		console.log('balance_portion_temp->', balance_portion_temp);
		console.log('rateportion_temp->',rateportion_temp);
		console.log('cal_val->', cal_val);

		frappe.model.set_value(cdt, cdn, 'wastage_amount', cal_val);
		console.log('cal_val->', cal_val);


    }
});

frappe.ui.form.on("Chef Prod Child Briyani", {
    product_qtykg:function(frm,cdt,cdn) {
		var d = locals[cdt][cdn];

		let product_qtykg_temp = 0;
		let portion_temp = 0;
		let portion_x_prod_qty_temp = 0;

		if(parseInt(d.product_qtykg)>=0)
			product_qtykg_temp = d.product_qtykg;

		if(parseInt(d.portion)>=0)
			portion_temp = d.portion;

		portion_x_prod_qty_temp = product_qtykg_temp * portion_temp;

		console.log('product_qtykg_temp->', product_qtykg_temp);
		console.log('portion_temp->',portion_temp);
		console.log('portion_x_prod_qty_temp->', portion_x_prod_qty_temp);

		frappe.model.set_value(cdt, cdn, 'portion_x_prod_qty', portion_x_prod_qty_temp);
    }
});


frappe.ui.form.on("Chef Prod Child Chicken", {
    wastage_pcs: function(frm,cdt,cdn) {
		var d = locals[cdt][cdn];

		let wastage_pcs_temp = 0;
		let rate_temp = 0;
		let cal_val = 0;

		if(parseInt(d.wastage_pcs)>=0)
			wastage_pcs_temp = d.wastage_pcs;

		if(parseInt(d.rate)>=0)
			rate_temp = d.rate;

		cal_val = wastage_pcs_temp * rate_temp;

		console.log('wastage_pcs_temp->', wastage_pcs_temp);
		console.log('rate_temp->',rate_temp);
		console.log('cal_val->', cal_val);

		frappe.model.set_value(cdt, cdn, 'wastage_amt', cal_val);
		// chicken category wastage amount total

		console.log('chicken category wastage amount total');
		var waste_total = 0;
		frm.doc.chicken_category_list.forEach(function(d) { waste_total += d.wastage_amt; });
		console.log('waste_total', waste_total);
		frm.set_value("chicken_category_wastage_amount", waste_total);
		refresh_field("chicken_category_wastage_amount");


    }
});

frappe.ui.form.on("Chef Prod Child Chicken", {
    rate: function(frm,cdt,cdn) {
		var d = locals[cdt][cdn];

		let wastage_pcs_temp = 0;
		let rate_temp = 0;
		let cal_val = 0;

		if(parseInt(d.wastage_pcs)>=0)
			wastage_pcs_temp = d.wastage_pcs;

		if(parseInt(d.rate)>=0)
			rate_temp = d.rate;

		cal_val = wastage_pcs_temp * rate_temp;

		console.log('wastage_pcs_temp->', wastage_pcs_temp);
		console.log('rate_temp->',rate_temp);
		console.log('cal_val->', cal_val);

		frappe.model.set_value(cdt, cdn, 'wastage_amt', cal_val);
    }
});

function disable_drag_drop_briyani_category_list(frm) {
		frm.page.body.find('[data-fieldname="briyani_category_list"] [data-idx] .data-row  .sortable-handle').removeClass('sortable-handle');
	}
function disable_drag_drop_chicken_category_list(frm) {
		frm.page.body.find('[data-fieldname="chicken_category_list"] [data-idx] .data-row  .sortable-handle').removeClass('sortable-handle');
	}
