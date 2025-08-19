
import frappe

def execute():
    airplane_ticket = frappe.get_all("Airplane Ticket",fields=["name", "seat"])
