// Copyright (c) 2024, Pubs and contributors
// For license information, please see license.txt

frappe.query_reports["Asset Master Register"] = {
	"filters": [
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
			"fieldname": "category_filter",
			"label": "Category",
			"fieldtype": "Data",
		},
		{
			"fieldname": "group_filter",
			"label": "Group",
			"fieldtype": "Link",
			"options": "Asset Master Group",
		},

	]
};
