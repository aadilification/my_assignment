# Copyright (c) 2025, yes and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns = [
		{'fieldname': 'airline','label':'Airline','fieldtype': 'Link','options': 'Airline'},
		{'fieldname': 'revenue','label':'Revenue','fieldtype': 'Currency','options': 'INR'}
	]

	airlines = frappe.get_all("Airplane Ticket", fields=["name","flight.airplane","total_amount"])

	# print("airlines", airlines)
	# output =  [{'name': 'IndiaGo-003-G56-to-J89-004', 'airplane': None, 'total_amount': 3800.0}]

	airlines_data = frappe.get_all("Airline", pluck='name')

	# print("airlines_data", airlines_data)
	# output = ['Sky Wings Airlines', 'Blue Horizon Air', 'Aero Nova', 'StarJet Airways', 'Pacific Fly']

	revenue_by_airline = {}
	for i in airlines_data:
		revenue_by_airline[i] = 0

		# print("revenue_by_airline", revenue_by_airline)
		# output =  {'Sky Wings Airlines': 0, 'Blue Horizon Air': 0, 'Aero Nova': 0, 'StarJet Airways': 0, 'Pacific Fly': 0}
	
	for a in airlines:
		airline = frappe.get_value("Airplane", a.airplane, "airline")
		# print("airline", airline)
		# output =  'Sky Wings Airlines'
		a["airline"] = airline
		frappe.errprint(a)
		frappe.errprint(a.airline)
		if a.airline in revenue_by_airline:
			revenue_by_airline[a.airline] += a.total_amount

		# print("revenue_by_airline", revenue_by_airline)
		# output =  {'Sky Wings Airlines': 3800.0, 'Blue Horizon Air': 0, 'Aero Nova': 0, 'StarJet Airways': 0, 'Pacific Fly': 0}

	data = [{"airline": k, "revenue": v} for k, v in revenue_by_airline.items()]
	frappe.errprint(data)
	chart = {
		"data": {
			"labels": [d['airline'] for d in data],
			"datasets": [{"name": "Revenue By Airline", "values": [d["revenue"] for d in data]}],
		},
		"type": "donut",
		"color": ["#33aadd", "#743ee2", "#feb019", "#a8152b", "#2f9e79", "#775dd0"],	
	}

	total_revenue = sum(d["revenue"] for d in data)
	
	# print("total_revenue", total_revenue)
	# output = total_revenue 122870.0	

	summery = [{
		"label": "Total Revenue",
		"value": total_revenue,
		"indicator": "Green" if total_revenue > 0 else "Red"
    
	}]

	return columns,data, None, chart, summery
