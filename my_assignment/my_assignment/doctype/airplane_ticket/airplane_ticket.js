// Copyright (c) 2025, yes and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Airplane Ticket", {
//     before_submit: function(frm) {
//         if (frm.doc.status !== "Boarded") {
//             frappe.validated = false; // stops submission
//             frappe.throw("You can only submit the ticket if the status is 'Boarded'.");
//         }
//     }
// });       


// frappe.ui.form.on('Airplane Ticket Add-on Item', {
//     item: function(frm, cdt, cdn) {
//         var d = locals[cdt][cdn];
//         $.each(frm.doc.add_ons, function(i, row) {
//             if (row.item === d.item && row.name != d.name) {
//                frappe.msgprint('This add-on item already exists in the list.');
//                frappe.model.remove_from_locals(cdt, cdn);
//                frm.refresh_field('add_ons');
//                return false;
//             }
//         });
//     }
// });


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


