// Copyright (c) 2025, yes and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airline", {
	refresh(frm) {
		frm.add_web_link(frm.doc.website, "Visit Website");
       
	}
	
});
