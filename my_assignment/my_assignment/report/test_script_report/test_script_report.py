# Copyright (c) 2025, yes and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns = [
		{'fieldname': 'airline','label':'Airline','fieldtype': 'Link','options': 'Airline'},
		{'fieldname': 'revenue','label':'Revenue','fieldtype': 'Currency','options': 'INR'}
	]

	airlines = frappe.get_all("Airline", pluck='name')
	print("airlines", airlines)
	total_revenue = 0
	data = []
	for airline in airlines:
		print("airline", airline)
		airplane_data = frappe.db.get_all('Airplane', pluck='name', filters={'airline': airline})
		print("airplane_data", airplane_data)
		flights = frappe.get_all('Airplane Flight', pluck='name', filters={'airplane': ['in', airplane_data]})
		# flights ['IndiaGo-003-08-2025']
		print("flights", flights)
		airplane_data = frappe.db.get_all(
			'Airplane Ticket',
			filters={'docstatus': 1, 'flight': ['in', flights]},
			fields=['sum(total_amount) as revenue']
		)
		print("airplane_data", airplane_data)
		# airplane_data [{'revenue': 4500.0}]
		# airplane_data [{'revenue': None}]
		if airplane_data:
			data.append({'airline': airline, 'revenue': airplane_data[0].revenue or 0})
			total_revenue += airplane_data[0].revenue or 0
	
	# print("data", data)

	chart = {
		"data": {
			"labels": [d['airline'] for d in data],
			"datasets": [{ "values": [d['revenue'] for d in data] }]
		},
		"type": "donut",
		"color": ["#7cd6fd", "#743ee2", "#feb019", "#ff4560", "#00e396", "#775dd0"],	
	}		

	summery = [{
		"label": "Total Revenue",
		"value": f"{total_revenue} INR",
		"indicator": "Green"
	}]

	return columns, data, None, chart, summery
