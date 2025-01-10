 frappe.ui.form.on("Stock Entry", {
	 	setup: function(frm){
  // compute total
      frm.compute_total = function(frm){
       console.log('total_price_temp');
		var total_price_temp = 0;
		frm.doc.raw_material_from_template.forEach(function(d) { total_price_temp += d.amount; });
		console.log('total_price_temp', total_price_temp);
		frm.set_value("total_price", total_price_temp);
        refresh_field('raw_material_from_template');
      }
	},
refresh(frm) {
		// frm.set_df_property('raw_material_list', 'cannot_add_rows', true);
		// frm.set_df_property('raw_material_list', 'cannot_delete_rows', true);
		// frm.set_df_property('raw_material_list', 'cannot_delete_all_rows', true);
		disable_drag_drop(frm);
		frm.add_custom_button(__('Load items from template'), function(){
			load_items_from_template_method(frm);
			},
							  );
	},
	onload(frm) {
		disable_drag_drop(frm);
		$('span.sidebar-toggle-btn').hide();
        $('.col-lg-2.layout-side-section').hide();

		frappe.form.link_formatters['Raw Material Only'] = function(value, doc) {
			if(doc.raw_material_text) {
				return doc.raw_material_text;
			}
			return value;
		}

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
		// 		let branch = res.message.branch_id;
		// 		let branch__name = res.message.branch_name;
		// 		frm.set_value('branch_id', branch);
		// 		frm.set_value('branch_name', branch__name);
		// 		frm.set_df_property('branch_name', 'read_only', 1);
		// 		console.log('branch_id-', branch, '=== branch_name-', branch__name);
  //
  //
		// 		frm.set_query("stock_entry_template", function() {
		// 			return {
		// 				"filters": {
		// 					"branch": branch
		// 				}
		// 			};
		// 		});
  //
		// 		frm.fields_dict["raw_material_from_template"].grid.get_field("raw_material").get_query = function(doc) {
		// 			return {
		// 				filters: {
		// 					'branch': frm.doc.branch_id,
		// 				}
		// 			}
		// 		};
  //
		// 			// =======
		// 			// let entry = frm.add_child("raw_material_from_template");
		// 			// entry.raw_material =  2;
		// 			// 	entry.item =  2;
		// 			// entry.unit = 'Kg';
		// 			// entry.price = 78;
		// 			frm.refresh_field("raw_material_from_template");
		// 			//frm.fields_dict[<fieldname>].disp_area.innerText = "Text to Display".
		// 			// =========
  //
		// 		}
		// 	});
		// 	//------------------------------------
		// };

	},


	// stock_entry_template: function(frm) {
	// 	if(frm.doc.stock_entry_template) {
	// 		console.log('stock_entry_template - succeeded ');
	// 		console.log(frm.doc.stock_entry_template);
	// 		let stock_entry_template_temp = frm.doc.stock_entry_template;
	// 		let branch = frm.doc.branch;
 //
	// 		//-- frappe call start --
	// 		frm.call({
	// 			doc: frm.doc,
	// 			method: 'get_raw_material',
	// 			args: {
	// 				branch: branch,
	// 				stock_entry_template: stock_entry_template_temp
	// 			},
	// 			freeze:true,
	// 			freeze_message: "Processing",
	// 			callback: function(r){
	// 				if (r.message) {
	// 					let msg = r.message;
 //
	// 					console.log(msg);
	// 					console.log('lenght',msg.length);
	// 					frm.doc.raw_material_from_template = [];
	// 					if (msg.length == 0){
	// 						frappe.show_alert("Raw materials are unavailable.");
	// 					}
	// 					else
	// 					{
	// 						$.each(msg, function(_i, e){
	// 							let entry = frm.add_child("raw_material_from_template");
	// 							//entry.raw_material = e[0];
	// 							console.log('before',entry);
	// 							console.log('***********************************');
	// 							console.log(e);
	// 							let raw_material_number =  Number(e[0]);
	// 							//entry.raw_material =  raw_material_number;
	// 							console.log(raw_material_number);
	// 							//entry.raw_material =  e[0];
	// 							entry.raw_material =  raw_material_number;
	// 							console.log(entry);
	// 							//pricechange
	// 							entry.unit = e[1];
	// 							entry.unit_price = e[2];
	// 							//pricechange
	// 							entry.unit_price_text = e[2];
	// 							entry.raw_material_text = e[3];
	// 							entry.clos_qty = e[4];
	// 							console.log('after',entry);
	// 						});
 //
 //
 //
	// 					}
	// 					frm.refresh_field("raw_material_from_template");
 //
	// 				}
	// 			}
	// 	    });
	// 		//-- frappe call end --
	// 	}
	// 	else {
	// 		console.log('stock_entry_template - failed ');
	// 		frm.doc.raw_material_from_template = [];
	// 		//refresh_field("raw_material_from_template");
	// 	}
	// },

});


 frappe.ui.form.on('Stock Entry Child', {
    form_render: function(frm,cdt,cdn) {
		console.log(' child row added event form_render');
    },
	ord_qty: function(frm,cdt,cdn) {
		// ord_qty_temp   unit_price_temp  amount_temp    total_price_temp
        var d = locals[cdt][cdn];
		let ord_qty_temp = 0;
		let unit_price_temp = 0;
		let cal_val = 0;


		ord_qty_temp = d.ord_qty;
		unit_price_temp = d.unit_price;

		cal_val = ord_qty_temp * unit_price_temp;

		console.log('balance_portion_temp->', ord_qty_temp);
		console.log('rateportion_temp->',unit_price_temp);
		console.log('cal_val->', cal_val);

		frappe.model.set_value(cdt, cdn, 'amount', cal_val);

		console.log('locals->', locals);
		console.log('cdt->', cdt);
		console.log('cdn->', cdn);
		console.log('d->', d);

		//total_price_temp
		frm.compute_total(frm);

    },
	raw_material_from_template_remove:function (frm, cdt, cdn) {
		console.log('raw_materials_remove');
		frm.compute_total(frm);
	}, //pricechange
	unit_price_text: function(frm,cdt,cdn) {
		console.log('unit_price_text')
        var d = locals[cdt][cdn];
		console.log('d->', d);
		frappe.model.set_value(cdt, cdn, 'unit_price', d.unit_price_text);
		//total_price_temp
		frm.compute_total(frm);

    },
	unit_price: function(frm,cdt,cdn) {
		console.log('unit_price')
        var d = locals[cdt][cdn];
		console.log('d->', d);
		//frappe.model.set_value(cdt, cdn, 'unit_price', d.unit_price_text);
		//total_price_temp

		let ord_qty_temp = 0;
		let unit_price_temp = 0;
		let cal_val = 0;
		ord_qty_temp = d.ord_qty;
		unit_price_temp = d.unit_price;
		cal_val = ord_qty_temp * unit_price_temp;

		console.log('balance_portion_temp->', ord_qty_temp);
		console.log('rateportion_temp->',unit_price_temp);
		console.log('cal_val->', cal_val);

		frappe.model.set_value(cdt, cdn, 'amount', cal_val);


		frm.compute_total(frm);

    },
});




function disable_drag_drop(frm) {
		frm.page.body.find('[data-fieldname="raw_material_list"] [data-idx] .data-row  .sortable-handle').removeClass('sortable-handle');
	}

// function filterChildFields(frm, tableName, fieldTrigger, fieldName, fieldFiltered) {
//     frm.fields_dict[tableName].grid.get_field(fieldFiltered).get_query = function(doc, cdt, cdn) {
//         var child = locals[cdt][cdn];
//         return {
//             filters:[
//                 [fieldName, '=', child[fieldTrigger]]
//             ]
//         }
//     }
// }


function load_items_from_template_method(frm){
		if(frm.doc.stock_entry_template) {

			let branch_selected = frm.doc.branch;
			let template_selected = frm.doc.stock_entry_template;
			console.log('branch_selected=',branch_selected);
			console.log('template_selected=',template_selected);

			//resolve_title_by_calling_api();
			//-- frappe call start --

			frm.call({
				doc: frm.doc,
				method: 'get_raw_material_with_id',
				args: {
					branch: branch_selected,
					template: template_selected
				},
				freeze:true,
				freeze_message: "Processing",
				callback: function(r){
					if (r.message) {
						let msg = r.message;

						console.log(msg);
						console.log('lenght',msg.length);
						frm.doc.raw_material_from_template = []
						if (msg.length == 0){
							frappe.show_alert("The template records for the Stock Entry Template could not be found.");
						}
						else
						{
							// ---- load start ------
							$.each(msg, function(_i, e){
								let entry = frm.add_child("raw_material_from_template");
								entry.raw_material = e[3];
								entry.unit = e[1];
								entry.unit_price = e[2];

								entry.raw_material_text = e[0];
								entry.unit_price_text = e[2];

							});
							// ------ load end --------
						}
						refresh_field("raw_material_from_template");
					}
				}
			});


			//-- frappe call end --
		} else {
			let msg = frappe.msgprint({
					title: 'Info',
					indicator: 'green',
					message: 'Please select the Stock Entry Template ',
					 primary_action:{
						'label': 'Close',
						action(values) {
							msg.hide();
						}
					}
				});

			console.log("no value in Stock Entry Template  ");
		}
	}
