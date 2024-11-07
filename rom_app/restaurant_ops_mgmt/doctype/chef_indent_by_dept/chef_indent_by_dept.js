frappe.ui.form.on("Chef Indent By Dept", {
	before_save: function(frm){

	},
	setup: function(frm){
      frm.compute_total = function(frm){
       console.log('total_price');
		var total_price = 0;
		frm.doc.raw_materials.forEach(function(d) { total_price += d.amount; });
		console.log('total_price', total_price);
		frm.set_value("total_price", total_price);
        refresh_field('raw_materials');
      }

	},
	refresh: function(frm) {
		disable_drag_drop(frm);
		// load items
		 frm.add_custom_button(__('Load items from template'), function(){
			 load_items_from_template_method(frm); }, );
		// load items
	},
	onload: function(frm) {
		disable_drag_drop(frm);
		$('span.sidebar-toggle-btn').hide();
        $('.col-lg-2.layout-side-section').hide();

		frappe.form.link_formatters['Raw Material Only'] = function(value, doc) {
			if(doc.raw_material_title) {
				return doc.raw_material_title;
			}
			return value;
		 }

		// if (frm.is_new()) {
  //
		//  }
	},

	department: function(frm) {
		console.log('department select');
	}
});


// Chef Indent By Dept Child  raw_materials
// branch_name department user_name date branch total_price raw_materials
// raw_material unit req_qty issued_qty price  amount closing_qty remarks
 frappe.ui.form.on('Chef Indent By Dept Child', {
  //   form_render: function(frm,cdt,cdn) {
		// console.log(' child row added event form_render');
  //   },
	issu_qty_entry: function(frm,cdt,cdn) {
		console.log('Chef Indent By Dept Child -> issu_qty_entry');
		// ord_qty_temp   unit_price_temp  amount_temp    total_price_temp
        var d = locals[cdt][cdn];
		let issued_qty = 0;
		let amount = 0;
		let cal_val = 0;
		let price = 0;
		//let float_issu_qty_entry = parseFloat(d.issu_qty_entry);
		//console.log(' float_issu_qty_entry - ', float_issu_qty_entry);
		//if(d.issu_qty_entry > 0) {
			console.log(' d.issu_qty_entry ', d.issu_qty_entry);


			if (d.issu_qty_entry == 0){
				issued_qty = 0;
			} else {
				issued_qty = (-1) * d.issu_qty_entry;
			}

			console.log(' after issued_qty', issued_qty);

			console.log('issued_qty ->',issued_qty);
			console.log('cdt ->',cdt);
			console.log('cdn ->',cdn);
			//frappe.model.set_value(cdt, cdn, "issued_qty", issued_qty);
			//refresh_field("raw_materials");
		// }
		//  else {
		// 	 console.log(' equal to 0');
		// 	 frappe.model.set_value(cdt, cdn, "issued_qty", 0);
		//  }

		// if(parseFloat(d.price)>=0)
			price = d.price;
			console.log(" price ", price);

		cal_val = issued_qty * price;
			console.log(" cal_val ", cal_val);

		console.log('issued_qty->', issued_qty,'price->',price,'cal_val->', cal_val);
		frappe.model.set_value(cdt, cdn, "amount", cal_val);
		frm.compute_total(frm);
		refresh_field("raw_materials");
    },
	raw_materials_remove:function (frm, cdt, cdn) {
		console.log('raw_materials_remove');
		frm.compute_total(frm);
	},
});


function disable_drag_drop(frm) {
		frm.page.body.find('[data-fieldname="raw_materials"] [data-idx] .data-row  .sortable-handle').removeClass('sortable-handle');
	}

function load_items_from_template_method(frm){
		if(frm.doc.department) {

			let branch_selected = frm.doc.branch;
			let dept_selected = frm.doc.department;
			console.log('branch_selected=',branch_selected);
			console.log('dept_selected=',dept_selected);

			//resolve_title_by_calling_api();
			//-- frappe call start --

			frm.call({
				doc: frm.doc,
				method: 'get_raw_material_with_id',
				args: {
					branch: branch_selected,
					department: dept_selected
				},
				freeze:true,
				freeze_message: "Processing",
				callback: function(r){
					if (r.message) {
						let msg = r.message;

						console.log(msg);
						console.log('lenght',msg.length);
						frm.doc.raw_materials = []
						if (msg.length == 0){
							frappe.show_alert("The template records for the department could not be found.");
						}
						else
						{
							// ---- load start ------
							$.each(msg, function(_i, e){
								let entry = frm.add_child("raw_materials");
								entry.raw_material = e[0];
								entry.unit = e[1];
								entry.raw_material_title = e[2];
								entry.price = e[3];
								//entry.closing_qty = e[4];
							});
							// ------ load end --------
						}
						refresh_field("raw_materials");
					}
				}
			});


			//-- frappe call end --
		} else {
			let msg = frappe.msgprint({
					title: 'Info',
					indicator: 'green',
					message: 'Please select the department',
					 primary_action:{
						'label': 'Close',
						action(values) {
							msg.hide();
						}
					}
				});

			console.log("no value in department ");
		}
	}
