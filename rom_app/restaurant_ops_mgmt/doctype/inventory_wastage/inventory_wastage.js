frappe.ui.form.on("Inventory Wastage", {
	setup: function(frm){
		// compute total
      frm.compute_total = function(frm){
		var total_price = 0;
		frm.doc.items.forEach(function(d) { total_price += d.amount; });
		console.log('total_price', total_price);
		frm.set_value("total_price", total_price);
        refresh_field('items');
	}
	},
	refresh(frm) {
		disable_drag_drop(frm);
	},
	onload(frm) {
		disable_drag_drop(frm);
		$('span.sidebar-toggle-btn').hide();
        $('.col-lg-2.layout-side-section').hide();
		console.log("onload");
		// if (frm.is_new()) {
		// 	console.log('is new - true')
		// 	let api_url = "rom_app.restaurant_ops_mgmt.api.get_the_branch_name_for_the_user"
		// 	let useremail = frappe.user.get_emails();
		// 	let email = useremail[0];
		// 	//------------------------------------
		// 	frappe.call({
		// 		method: api_url,
		// 		args: {emailid: email},
		// 		callback: function(res) {
		// 			let branch__id = res.message.branch_id;
		// 			let branch__name = res.message.branch_name;
		// 			frm.set_value('branch_id', branch__id);
		// 			frm.set_value('branch_name', branch__name);
		// 			frm.set_df_property('branch_name', 'read_only', 1);
		// 			console.log('brnach id - '+ branch__id + ' = branch_name - ' + branch__name );
  //
		// 			frm.fields_dict["items"].grid.get_field("raw_material").get_query = function(doc) {
		// 			return {
		// 				filters: {
		// 					'branch': branch__id,
		// 				}
		// 			}
		// 		}
		// 		}
		// 	});
		// 	//------------------------------------
		// } else {
		// 		let branch__id = frm.doc.branch_id;
		// 		frm.fields_dict["items"].grid.get_field("raw_material").get_query = function(doc) {
		// 			return {
		// 				filters: {
		// 					'branch': branch__id,
		// 				}
		// 			}
		// 		}
		// }

		disable_drag_drop(frm);
	},
});




 frappe.ui.form.on('Inventory Wastage Child', {
    form_render: function(frm,cdt,cdn) {
		console.log(' child row added event form_render');
        //let item = locals[cdt][cdn];
       // let articleId = Math.round(+new Date()/1000);
       // item.article_id = articleId;
		//console.log('item',item);

       //item.refresh_field('raw_material');
    },
	waste_qty_entry: function(frm,cdt,cdn) {
		/*
		Inventory Wastage Child  items
		branch_name user_name date branch_id total_price
		raw_material unit wastage_qty unit_price  amount clos_stock
		*/
        var d = locals[cdt][cdn];
		let wastage_qty = 0;
		let unit_price = 0;
		let cal_val = 0;

		//if(parseFloat(d.wastage_qty)>=0)
			wastage_qty = (-1) * d.waste_qty_entry;

		//if(parseFloat(d.unit_price)>=0)
			unit_price = d.unit_price;

		cal_val = wastage_qty * unit_price;
		//cal_val = cal_val * -1;

		console.log('wastage_qty->', wastage_qty);
		console.log('unit_price->',unit_price);
		console.log('cal_val->', cal_val);

		frappe.model.set_value(cdt, cdn, 'wastage_qty', wastage_qty);

		frappe.model.set_value(cdt, cdn, 'amount', cal_val);

		console.log('locals->', locals);
		console.log('cdt->', cdt);
		console.log('cdn->', cdn);
		console.log('d->', d);

		//total_price_temp
		console.log('total_price_temp');
		frm.compute_total(frm);
    },
	items_remove:function (frm, cdt, cdn) {
		console.log('items_remove');
		frm.compute_total(frm);
	},
});

function disable_drag_drop(frm) {
		frm.page.body.find('[data-fieldname="items"] [data-idx] .data-row  .sortable-handle').removeClass('sortable-handle');
	}
