frappe.ui.form.on("Inventory Counting", {
	setup: function(frm){
		// compute total
      frm.compute_total = function(frm){
		var total_amount = 0;
		frm.doc.items.forEach(function(d) { total_amount += d.amount; });
		console.log('total_amount', total_amount);
		frm.set_value("total_amount", total_amount);

		refresh_field("items");
	  }
	},
	refresh(frm) {
		disable_drag_drop(frm);

	},
	onload(frm) {
		disable_drag_drop(frm);
		$('span.sidebar-toggle-btn').hide();
        $('.col-lg-2.layout-side-section').hide();

		// if (frm.is_new()) {
		// 	console.log('is_new');
		// 	let useremail = frappe.user.get_emails();
		// 	let email = useremail[0];
		// 	console.log('email ',email);
		// 	let api_url = "rom_app.restaurant_ops_mgmt.api.get_the_branch_name_for_the_user"
		// 	//------------------------------------
		// 	frappe.call({
		// 	method: api_url,
		// 	args: {emailid: email},
		// 	callback: function(res) {
		// 		let branch__id = res.message.branch_id;
		// 		let branch__name = res.message.branch_name;
		// 		frm.set_value('branch_id', branch__id);
		// 		frm.set_value('branch_name', branch__name);
		// 		frm.set_df_property('branch_name', 'read_only', 1);
		// 		console.log('branch_id-', branch__id, '=== branch_name-', branch__name);
  //
  //
  //
		// 		frm.fields_dict["items"].grid.get_field("raw_material").get_query = function(doc) {
		// 			return {
		// 				filters: {
		// 					'branch': branch__id,
		// 				}
		// 			}
		// 		}
  //
		// 		}
		// 	});
		// } else {
		// 	let branch__id = frm.doc.branch_id;
		// 	frm.fields_dict["items"].grid.get_field("raw_material").get_query = function(doc) {
		// 			return {
		// 				filters: {
		// 					'branch': branch__id,
		// 				}
		// 			}
		// 		}
  //
		// }
    },
});


frappe.ui.form.on("Inventory Counting Child", {
// items total_amount
// raw_material  unit  price  clos_stock  quantity  diff  amount
    quantity:function(frm,cdt,cdn) {
		console.log("----clos_stock---");
		var d = locals[cdt][cdn];

		let price = 0;
		let counted_quantity = 0;
		let cal_val = 0;
		let cal_amount = 0;
		let counted_quantity_temp = 0;
		let clos_stock = 0;

		price = parseFloat(d.price);
		counted_quantity_temp = parseFloat(d.quantity);
		clos_stock = parseFloat(d.clos_stock);

		if(clos_stock >= 0)
			cal_val =  counted_quantity_temp - clos_stock;
		else
			cal_val =  counted_quantity_temp + clos_stock;

		console.log('clos_stock_temp->', clos_stock);
		console.log('counted_quantity_temp->',counted_quantity_temp);
		console.log('cal_val->', cal_val);
		frappe.model.set_value(cdt, cdn, 'diff', cal_val);

		cal_amount = counted_quantity_temp * price;
		console.log('price->',price);
		console.log('cal_val->', cal_val);
		console.log('cal_amount->', cal_amount);
		frappe.model.set_value(cdt, cdn, 'amount', cal_amount);

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
