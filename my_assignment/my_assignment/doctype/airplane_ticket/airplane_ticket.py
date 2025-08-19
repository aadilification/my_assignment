# Copyright (c) 2025, yes and contributors
# For license information, please see license.txt

# import frappe
# import random
# from frappe.model.document import Document


# class AirplaneTicket(Document):
# 	def before_save(self):
# 		 # Auto-assign seat if not already assigned.
# 		if not self.seat:
# 			self.seat = self.generate_seat()
	
# 		# self.total_amount = self.flight_price * 5
# 		self.calculate_amount()

# 		items = self.add_ons
# 		unique_items = []
# 		item_codes = set()

# 		for row in items:
# 			if row.item not in item_codes:
# 				item_codes.add(row.item)
# 				unique_items.append(row)
			
# 		self.item = unique_items

# 	def calculate_amount(self):
# 		total_amount = 0
# 		if not self.add_ons:
# 			self.total_amount = self.flight_price
# 			frappe.errprint(self.total_amount)

# 		else:
# 			for add_on in self.add_ons:
# 				total_amount = total_amount + add_on.amount
# 				# frappe.errprint(total_amount)

# 			self.total_amount = total_amount + self.flight_price
# 			# frappe.errprint(self.total_amount)

			

# 	def before_submit(self):
# 		if self.status != 'Boarded':
# 			frappe.throw('The status is not equal to Boarded.')


# 	# def validate(self):
# 	# 	flight_price = self.flight_price or 0
# 	# 	addons_total = 0

# 	# 	for addon in self.add_ons:
# 	# 		addons_total += addon.amount or 0
# 	# 	self.total_amount = flight_price + addons_total

# 	def generate_seat(self):

#         #Generate a random seat in format like 2A, 31C, etc.

# 		row = random.randint(1, 50)	# Example: rows 1 to 50
# 		seat_letter = random.choice(["A", "B", "C", "D", "E", "F"])
# 		return f"{row}{seat_letter}"
	
# 	# def validate_add_ons(self):
# 	# 	doc = frappe.get_doc("Airplane Ticket", self.name)
# 	# 	dict_of_add_ons = []
# 	# 	for add_on in doc.add_ons:
# 	# 		if add_on in dict_of_add_ons:
# 	# 			frappe.throw("Lead Owner cannot be same as the Lead Email Address")
# 	# 		else:
# 	# 			dict_of_add_ons.append(add_on.item)

# class AirplaneTicket(Document):

#     def validate(self):
#         self.validate_add_ons()

#     def validate_add_ons(self):
#         seen = set()
#         for add_on in self.add_ons:
#             if add_on.item in seen:
#                 frappe.throw(_("Add-ons '{0}' is duplicated. Each add-on must be unique.").format(add_on.item))
#             seen.add(add_on.item)

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
    def validate_add_ons(self):
        seen = set()
        for add_on in self.add_ons:
            if add_on.item in seen:
                frappe.throw(
                    _("Add-ons '{0}' is duplicated. Each add-on must be unique.").format(add_on.item),
                    frappe.ValidationError
                )
            seen.add(add_on.item)
