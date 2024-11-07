// Copyright (c) 2024, Pubs and contributors
// For license information, please see license.txt

frappe.query_reports["Menu Register"] = {
	"filters": [
	    {
			"fieldname": "branch_filter",
			"label": "Branch",
			"fieldtype": "Link",
			"options": "Branch",
		},
		{
			"fieldname": "menu_item_filter",
			"label": "Menu Item",
			"fieldtype": "Data"
		},
		{
			"fieldname": "menu_group_filter",
			"label": "Menu Group",
			"fieldtype": "Link",
			"options": "Menu Group",
		},
	]
};
