frappe.pages['bankimport'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __('Bank Import'),
		single_column: true
	});

	frappe.bankimport.make(page);
	// frappe.bankimport.run();
}

frappe.bankimport = {
	start: 0,
	make: function(page) {
		var me = frappe.bankimport;
		me.page = page;
		me.body = $('<div></div>').appendTo(me.page.main);
		var data = "";
		$(frappe.render_template('bankimport', data)).appendTo(me.body);

		// attach button handlers
		this.page.main.find(".btn-parse-file").on('click', function() {
			var me = frappe.mycalc;
			
			// get bank
			var bank = $('#bank').val();
			
			// read the file 
			var file = document.getElementById("input_file").files[0];
			var content = "";
			if (file) {
				// create a new reader instance
				var reader = new FileReader();
				// assign load event to process the file
				reader.onload = function (event) {
					// read file content
					content = event.target.result;
					
					// call bankimport method with file content
					frappe.call({
						method: 'myapp.myapp.page.bankimport.bankimport.parse_file',
						args: {
							content: content,
							bank: bank
						},
						callback: function(r) {
							if (r.message) {
								var parent = page.main.find(".insert-log-messages").empty();
								$('<p>Logged!</p>').appendTo(parent);
								frappe.msgprint(r.message.message);
							} 
						}
					}); 
				}
				// assign an error handler event
				reader.onerror = function (event) {
					frappe.msgprint(__("Error reading file"), __("Error"));
				}
				
				reader.readAsText(file, "UTF-8");
			}
			else
			{
				frappe.msgprint(__("Please select a file."), __("Information"));
			}
			

		});
	},
	run: function() {
		
	}
}
