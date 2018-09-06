frappe.listview_settings['MyLabel'] = {
	colwidths: {"subject": 6},
	onload: function(listview) {
		listview.page.add_menu_item(__("Set as Open"), function() {
			listview.call_for_selected_items(method, {"status": "Open"});
		});

		listview.page.add_menu_item(__("Set as Closed"), function() {
			listview.call_for_selected_items(method, {"status": "Closed"});
		});
        
        /* // does not work
        listview.page.add_custom_button(__('Hello'), function() {
            frappe.msgprint("Hello World");
        })*/
	}
}
