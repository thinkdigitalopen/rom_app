
frappe.query_reports["Asset Count Register"] = {
	"filters": [
		{
			"fieldname": "from_date_filter",
			"label": "From Date *",
			"fieldtype": "Date",
			"default": frappe.datetime.add_days(frappe.datetime.get_today(), -1),
			"mandatory": 1,
		},
		{
			"fieldname": "to_date_filter",
			"label": "To Date *",
			"fieldtype": "Date",
			"default": frappe.datetime.now_date(),
			"mandatory": 1,
		},
		{
			"fieldname": "branch_filter",
			"label": "Branch",
			"fieldtype": "Link",
			"options": "Branch",
		},
		{
			"fieldname": "item_filter",
			"label": "Item",
			"fieldtype": "Data",
		},
		{
			"fieldname": "group_filter",
			"label": "Group",
			"fieldtype": "Link",
			"options": "Asset Master Group",
		},
		{
			"fieldname": "diff_filled_filter",
			"label": "Diff Filled",
			"fieldtype": "Check"
		},
	]
};
