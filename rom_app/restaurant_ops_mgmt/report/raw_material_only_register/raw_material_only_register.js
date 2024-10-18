// Copyright (c) 2024, Pubs and contributors
// For license information, please see license.txt

frappe.query_reports["Raw Material Only Register"] = {
	"filters": [
        {
			"fieldname": "branch_filter",
			"label": "Branch",
			"fieldtype": "Link",
			"options": "Branch",
		},
		{
			"fieldname": "raw_material_filter",
			"label": "Raw Material",
			"fieldtype": "Data",
		},
		{
			"fieldname": "group_name_filter",
			"label": "RM Group",
			"fieldtype": "Link",
			"options": "Raw Material Group",
		},
	]
};
