# Copyright (c) 2025, yes and contributors
# For license information, please see license.txt

import frappe
import random
from frappe.model.document import Document
from frappe import _

class AirplaneTicket(Document):
    def before_save(self):
        # Auto-assign seat if not already assigned
        if not self.seat:
            self.seat = self.generate_seat()

        # Calculate total amount
        self.calculate_amount()

        # Ensure add-ons are unique
        self.validate_add_ons()

    def calculate_amount(self):
        flight_price = self.flight_price or 0
        addons_total = sum([add_on.amount or 0 for add_on in self.add_ons]) if self.add_ons else 0
        self.total_amount = flight_price + addons_total

    def before_submit(self):
        if self.status != "Boarded":
            frappe.throw(
                _("Ticket cannot be submitted unless status is 'Boarded'."),
                frappe.ValidationError
            )

    def generate_seat(self):
        """Generate a random seat in format like 2A, 31C, etc."""
        row = random.randint(1, 50)  # Example: rows 1 to 50
        seat_letter = random.choice(["A", "B", "C", "D", "E", "F"])
        return f"{row}{seat_letter}"
    # to validate add-ons
    # add-ons must be unique
    def validate_add_ons(self):
        seen = set()
        for add_on in self.add_ons:
            if add_on.item in seen:
                frappe.throw(
                    _("Add-ons '{0}' is duplicated. Each add-on must be unique.").format(add_on.item),
                    frappe.ValidationError
                )
            seen.add(add_on.item)

    def validate(self):
        flight = frappe.get_doc("Airplane Flight", self.flight)
        # print("flight", flight)
        airplane = frappe.get_doc("Airplane", flight.airplane)
        # print("airplane capacity", airplane.capacity)   #2

        booked_tickets = frappe.db.count("Airplane Ticket", {"flight": self.flight, "docstatus":["<", 2]})
        # print("booked tickets", booked_tickets) #2

        if booked_tickets >= airplane.capacity:
            frappe.throw(
                _("Cannot book ticket. Flight '{0}' is at full capacity.").format(self.flight)
            )


