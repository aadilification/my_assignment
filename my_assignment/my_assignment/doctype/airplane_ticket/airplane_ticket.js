// Copyright (c) 2025, yes and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
    before_submit: function(frm) {
        if (frm.doc.status !== "Boarded") {
            frappe.validated = false;  // stop submission
            frappe.throw("You can only submit the ticket if the status is 'Boarded'.");
        }
    }
});

frappe.ui.form.on("Airplane Ticket Add-on Item", {
    item: function(frm, cdt, cdn) {
        let d = locals[cdt][cdn];
        let duplicate = frm.doc.add_ons.filter(row => row.item === d.item && row.name !== d.name);

        if (duplicate.length > 0) {
            frappe.msgprint(`Add-on item "${d.item}" already exists.`);
            frappe.model.remove_from_locals(cdt, cdn);
            frm.refresh_field("add_ons");
        }
    }
});

frappe.ui.form.on("Airplane Ticket", {
   refresh: function(frm) {
       frm.add_custom_button(__('Assign Seat'), function() {
            let dialog = new frappe.ui.Dialog({
                title:"Enter Seat Number",
                fields:[
                    {
                        label: "Seat",
                        fieldname: "seat",
                        fieldtype: "Data"
                    }
                ],
                primary_action_label: "Assign",
                primary_action(values){
                    console.log(values);
                    frm.set_value("seat", values.seat);
                    dialog.hide();
                    frm.save();
                    
                }
            })
            dialog.show();
        }, __("Actions"));
   }
});


