# Copyright (c) 2025, yes and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
	def before_submit(self):
		self.status = "Completed"

	def before_save(self):
		# if self.has_value_changed("gate_number"):
			# print(f"before save - Gate number changed to {self.gate_number}")
			# output =  before save - Gate number changed to G03
		
		self.validate_crew()
	def validate_crew(self):
		seen = set()
		for i in self.crew:
			if i.crew_members in seen:
				frappe.throw(
					("Crew '{0}' is duplicated. Each crew must be unique.").format(i.crew_members),
					frappe.ValidationError
				)
			seen.add(i.crew_members)

	def on_update(self):
		if self.has_value_changed("gate_number"):
			# print(f"on update - Gate number changed to {self.gate_number}")
			# output =  on update - Gate number changed to G03

			tickets = frappe.get_all(
				"Airplane Ticket",
				filters={"flight": self.name},
				pluck="name"
			)
		
			# print("tickets", tickets)
			# ['ticket1', 'ticket2', 'ticket3']

			for ticket in tickets:
				frappe.db.set_value(
					"Airplane Ticket",
					ticket,
					"gate_number",
					self.gate_number
				)
				# print(f"Updated gate number to {self.gate_number} for ticket {ticket}")
				# output = Updated gate number to G03 for ticket ticket1
				frappe.logger().info(f"Updated gate number to {self.gate_number} for {len(tickets)} tickets of flight {self.name}")
		
		
