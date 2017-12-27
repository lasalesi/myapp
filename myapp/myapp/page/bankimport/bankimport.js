frappe.pages['bankimport'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __('BankImport'),
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
			// var file = $('#input_file').val();
			// var file = document.getElementById('input_file').files[0];
			
			// read the file 
			var file = document.getElementById("input_file").files[0];
			var content = "";
			window.alert("Has a file");
			if (file) {
				var reader = new FileReader();
				reader.onload = function (event) {
					// document.getElementById("fileContents").innerHTML = event.target.result;
					content = event.target.result;
					window.alert("Content: " + content);
					
					frappe.call({
						method: 'myapp.myapp.page.bankimport.bankimport.parse_file',
						args: {
							content: content
						},
						callback: function(r) {
							if(r.message) {
								/*this.page.main.find(".insert-log").removeClass("hide");
								var parent = this.page.main.find(".insert-log-messages").empty();
								$('<p>Logged!</p>').appendTo(parent);*/
								frappe.msgprint("File parsed.");
							} 
						}
					}); 
				}
				reader.onerror = function (event) {
					document.getElementById("fileContents").innerHTML = "error reading file";
				}
				
				reader.readAsText(file, "UTF-8");
			}
			

		});
	},
	run: function() {
		
	}
}
