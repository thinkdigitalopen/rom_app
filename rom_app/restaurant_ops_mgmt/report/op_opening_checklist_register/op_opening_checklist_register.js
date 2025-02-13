frappe.query_reports["Op Opening Checklist Register"] = {
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
			"fieldname": "audit_filter",
			"label": "Audit",
			"fieldtype": "Select",
			"options": "\nYes\nNo"
		},
		{
			"fieldname": "area_filter",
			"label": "Area",
			"fieldtype": "Data",
		},
		{
			"fieldname": "question_filter",
			"label": "Question",
			"fieldtype": "Data",
		}
	]
};
