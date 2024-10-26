frappe.pages['checklist-matrix'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Checklist Matrix',
		single_column: true
	});

 	insert_datatable_holder_div();
 	build_header_ui();

	function insert_datatable_holder_div()
	{
		$("<div class='datatable'></div>").appendTo('.layout-main-section');
	}

	function draw_datatable_json(dict)
	{
		console.log(' draw_datatable_json ');
		console.log(dict);

		array2d = convert_arr_object_to_2d_array(dict);
		console.log(array2d);

		console.log('columns start');
		let columns = get_columns_from_2darray(array2d);
		console.log('columns end ', columns);

		let columns_frappetable = get_columns_from_2darray_for_frappetable(columns);
		console.log('columns_frappetable ',columns_frappetable);

		let data_frappetable = get_data_from_2darray_for_frappetable(array2d, columns);
		console.log(data_frappetable);

		const datatable = new DataTable('.datatable', {
			columns: columns_frappetable,
			data: data_frappetable
		});
		datatable.refresh(data_frappetable,columns );
	}

	function get_data_from_2darray_for_frappetable(array2d, columns)
	{
		const rowCount = array2d.length;
		const  columnCount= array2d[0].length;

		console.log(rowCount);
		console.log(columnCount);

		let data = [];
		let key = 0;
		let val = 0;
		for(var i=0; i<rowCount; i++ )
		{
			//skip the first row because it has headers
			if (i == 0) continue;
			let row = {};
			for(var j=0; j<columnCount; j++ )
			{
				key = columns[j];
				val =  array2d[i][j];

				if (val == 1) val = '&#10003;';
				if (val == 0) val = '';

				row[key] = val;
			}
			data.push(row);
		}

		return data;
	}

	function convert_arr_object_to_2d_array(arr)
	{
		const dates = Object.keys(arr).filter(key => key !== 'name' && key !== 'question');
		const headers = ['name', 'question', ...dates];

		const result = [headers];
		for (let i = 0; i < Object.keys(arr.name).length; i++)
		{
			const row = [
				arr.name[i],
				arr.question[i],
				...dates.map(date => arr[date][i])
			];
			result.push(row);
		}
		return result;
	}

	function get_columns_from_2darray_for_frappetable(columns)
	{
		let columns_frappe = [];

		for(var i=0; i<columns.length; i++)
		{
			let column	= { name: columns[i] , editable:false, focusable:false };
			columns_frappe.push(column);
		}

		return columns_frappe;
	}

	function get_columns_from_2darray(arr)
	{
		const rowCount = arr.length;
		console.log(rowCount);

		const columnCount = arr[0].length;
		console.log(columnCount);

		let columns = [];
		let header_row = arr[0];

		for(var j=0; j<columnCount; j++)
		{
			columns.push(header_row[j]);
		}
		return columns;
	}


	function get_data(){
		let api_url = "rom_app.restaurant_ops_mgmt.api_checklist_matrix.get_checklist_matrix_data";
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

	function build_header_ui()
	{

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
						' ',
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
						draw_datatable_json(res);
					}
				});
	 }

	function global_get_to_date()
	{
		var from_date_temp = frappe.datetime.now_date();
		return from_date_temp;
	}

	function global_get_from_date()
	{
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


