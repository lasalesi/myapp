frappe.pages['payment_export'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __('Payment Export'),
		single_column: true
	});

	frappe.payment_export.make(page);
	frappe.payment_export.run();
}

frappe.payment_export = {
	start: 0,
	make: function(page) {
		var me = frappe.payment_export;
		me.page = page;
		me.body = $('<div></div>').appendTo(me.page.main);
		var data = "";
		$(frappe.render_template('payment_export', data)).appendTo(me.body);

		// attach button handlers
		this.page.main.find(".btn-create-file").on('click', function() {
			var me = frappe.payment_export;
			
		

		});
	},
	run: function() {

	}
}
