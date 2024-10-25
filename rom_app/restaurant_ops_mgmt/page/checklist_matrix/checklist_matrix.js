frappe.pages['checklist-matrix'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Checklist Matrix',
		single_column: true
	});

	insert_datatable_holder_div();
	build_header_ui();

	function insert_datatable_holder_div(){
		    $("<div class='datatable'></div>").appendTo('.layout-main-section');
	}
	function draw_datatable(dict){

		let dataarray = [];
		let columns = [];
		let l_row = 0;
		let l_col = 0;

		let dict_length = dict.length;
		console.log('dict_length');
		console.log(dict_length);

		let trans_array_col_length = 0;
		$.each(dict, function(_i, e){
			console.log('_i');
			console.log(_i);
			console.log(e);
			let column	= { name: _i, editable:false, focusable:false };
			columns.push(column);
			console.log('l_row ',l_row);
			dataarray[l_row] = e;
			l_row = l_row + 1;

			trans_array_col_length = Object.keys(e).length;
		});

		console.log('dataarray');
		console.log(dataarray);


	console.log(columns);
		console.log(columns.length);
		let col_len = columns.length;

		console.log(' looping array ');

		//var transarray = [];

		//string transarray[][] = new string[][];
		var transarray =  Array.apply(null, Array(col_len)).map(e => Array(trans_array_col_length));

		for(var i=0;i<dataarray.length; i++ )
		{
			console.log('i',i);
			console.log(dataarray[i]);
			var itemarray = dataarray[i];

			console.log( 'item array length - ', Object.keys(itemarray).length);

			console.log('--- itemarray  loop START -- ',i);
			let j = 0;
			for (let key in itemarray) {

				console.log('key - ', key, itemarray[key]);
				console.log('temarray[key] - ', itemarray[key]);
				console.log('i --> j',i,'  ', j);
				//transarray[i][j] = itemarray[key];
				transarray[i].push(itemarray[key]);
				//transarray.push(i, itemarray[key])
				j = j+1;
			}
			console.log('--- itemarray  loop END -- ',i);
			console.log('transarray');
			console.log(transarray);

			// for(var j=0;j<itemarray.length; j++ )
			// {
			// 	transarray[i][j] = itemarray[j];
			// }
		}

		console.log(' transarray');
		console.log(transarray);

// 		columns = [
//
//             {name:'Position', editable:false, focusable:false},
//             {name:'Salary', editable:false, focusable:false},
//         ]

		// let data = [];
		// let row = [];
		//let row_length = dict.length;
		//console.log('row_length - ',row_length);


/*
		$.each(dict, function(_i, e)
		{
			let row_length = e.length;
			console.log('row_length - ',row_length);
			var row = {};
			for(var m=0;m<row_length; m++)
			{
				row[m]=e[m];
			}
			console.log('row ',row);

		}
		);*/
//data.push(row);
//
// 		let rr = {
//                 'Name':'raj',
//                 'Position':'supplier',
//                 'Salary':'100',
//             }
//
//         let rr2 = {
//                 'Name':'raj2',
//                 'Position':'supplier2',
//                 'Salary':'1002',
//             }
		// for(i=0;i< )
		// for(var j=0;j<itemarray.length; j++ )
		// {
		// 	transarray[i][j] = itemarray[j];
		// }

		// data.push(rr);
		// data.push(rr2);

		// const datatable = new DataTable('.datatable', {
		// 	columns: columns,
		// 	data: transarray
		// });
		//datatable.refresh(data,columns );
	}

	function get_data(){
		let api_url = "rom_app.restaurant_ops_mgmt.api_checklist_matrix.get_checklist_matrix_data";
		// frappe.call({
		// 	method: api_url,
		// 	args: {'branch': '', 'checklist_type': '', 'from_date': '','to_date': ''},
		// 	async: false;
		// 	callback: function(res) {
		// 		console.log(res);
		// 	}
		// });
		let result_data = [];
		frappe.call({
			method: api_url,
			args: {
			'branch': '',
			'checklist_type': '',
			'from_date':'',
			'to_date':'',
			},
			async: false,
			callback: function(res) {
				console.log(res);
				result_data = res.message;

			}
		});
		return result_data;
	}

	function build_header_ui(){

		let from_date = global_get_from_date();
		let to_date = global_get_to_date();

		page.add_field({
					label: "Branch",
					fieldtype: 'Select',
					fieldname: 'field_branch',
					options: [
						'',
						'HPMadurai',
						'HPChennai'
					],
				});

		page.add_field({
					label: "Checklist",
					fieldtype: "Select",
					fieldname: "field_checklist",
					options: [
						'',
						'FB Opening',
						'FB Closing',
						'Op Opening',
						'Op Closing'
					],
				});

		page.add_field({
					label: "From Date",
					default: from_date,
					fieldtype: 'Date',
					fieldname: 'field_fromdate',
				});

		page.add_field({
					label: "To Date",
					default: to_date,
					fieldtype: 'Date',
					fieldname: 'field_todate',
				});

		page.add_field({
					label: "Submit",
					fieldtype: 'Button',
					fieldname: 'field_submit',
					click(){
						console.log('clicked');
						let res = get_data();
						console.log(res);
						draw_datatable(res);
					}
				});
	 }

	 function global_get_to_date(){
		var from_date_temp = frappe.datetime.now_date();
		return from_date_temp;
	}

	function global_get_from_date(){
		var from_date_temp = global_get_to_date();
		var from_date_minus_one = new Date(frappe.datetime.str_to_obj(from_date_temp));
		from_date_minus_one.setDate(from_date_minus_one.getDate() - 1);

		let date_only = from_date_minus_one.getDate();
		let month_only = from_date_minus_one.getMonth() + 1;
		if (month_only.toString().length == 1) {
            month_only = "0" + month_only;
        }
		let year_only = from_date_minus_one.getFullYear();

		var from_date_minus_one_opt = year_only + "-" + month_only + "-" + date_only;

		console.log("^^^^^^^^^^^^^^^^^^^^^^^");
		console.log(" date_only=",date_only);
		console.log(" month_only=",month_only);
		console.log(" year_only=",year_only);

		console.log("from_date_minus_one_opt", from_date_minus_one_opt);
		return from_date_minus_one_opt;
	}
}
