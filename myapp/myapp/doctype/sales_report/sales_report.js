// Copyright (c) 2018, lasalesi and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Report', {
	refresh: function(frm) {

	},
    setup: function(frm) {
        frappe.call({
            method: 'fill',
            doc: frm.doc,
            callback: function(response) {
                refresh_field(['items', 'week', 'date']);
            }
        }); 
    }
});
