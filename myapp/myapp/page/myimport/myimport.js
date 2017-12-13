frappe.pages['myimport'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __('MyImport'),
		single_column: true
	});

	frappe.myimport.make(page);
	// frappe.myimport.run();
	//this.make_upload();
}

frappe.myimport = {
	start: 0,
	make: function(page) {
		var me = frappe.myimport;
		me.page = page;
		me.body = $('<div></div>').appendTo(me.page.main);
		// me.body = $('<div></div>' + '<h1>Hello World!</h1>').appendTo(me.page.main);
		var data = "MyImport";
		$(frappe.render_template('myimport', data)).appendTo(me.body);

		/* me.more = $('<div class="for-more"><button class="btn btn-sm btn-default btn-more">'
			+ __("More") + '</button></div>').appendTo(me.page.main)
			.find('.btn-more').on('click', function() {
				me.start += 40;
				me.run();
			}); */

		this.page.main.find(".btn-import").on('click', function() {
			window.alert("Alright, not yet implemented");
		});
	},
	make_upload: function() {
		var me = this;
		frappe.upload.make({
			no_socketio: true,
			parent: this.page.main.find(".upload-area"),
			btn: this.page.main.find(".btn-import"),
			get_params: function() {
				return {
					ignore_encoding_errors: me.page.main.find('[name="ignore_encoding_errors"]').prop("checked"),
					from_data_import: 'Yes'
				}
			},
			args: {
				method: 'frappe.core.page.data_import_tool.importer.upload',
			},
			allow_multiple: 0,
			onerror: function(r) {
				//me.onerror(r);
			},
			queued: function() {
				// async, show queued
				msg_dialog.clear();
				frappe.msgprint(__("Import Request Queued. This may take a few moments, please be patient."));
			},
			running: function() {
				// update async status as running
				msg_dialog.clear();
				frappe.msgprint(__("Importing..."));
				me.write_messages([__("Importing")]);
				me.has_progress = false;
			},
			progress: function(data) {
				// show callback if async
				if(data.progress) {
					frappe.hide_msgprint(true);
					me.has_progress = true;
					frappe.show_progress(__("Importing"), data.progress[0],
						data.progress[1]);
				}
			},
			callback: function(attachment, r) {
				if(r.message.error || r.message.messages.length==0) {
					me.onerror(r);
				} else {
					if(me.has_progress) {
						frappe.show_progress(__("Importing"), 1, 1);
						setTimeout(frappe.hide_progress, 1000);
					}

					r.messages = ["<h5 style='color:green'>" + __("Import Successful!") + "</h5>"].
						concat(r.message.messages)

					me.write_messages(r.messages);
				}
			},
			is_private: true
		});

		frappe.realtime.on("data_import_progress", function(data) {
			if(data.progress) {
				frappe.hide_msgprint(true);
				me.has_progress = true;
				frappe.show_progress(__("Importing"), data.progress[0],
					data.progress[1]);
			}
		})

	},
	run: function() {
		var me = frappe.myimport;
		frappe.call({
			method: 'myapp.myimport.get_data',
			args: {
				start: me.start
			},
			callback: function(r) {
				if(r.message) {
					r.message.forEach(function(d) {
						me.add_row(d);
					});
				} else {
					frappe.show_alert({message:__('No more updates'), indicator:'darkgrey'});
					me.more.parent().addClass('hidden');
				}
			}
		});
	},
	add_row: function(data) {
		var me = frappe.myimport;

		data.by = frappe.user.full_name(data.sender);
		data.avatar = frappe.avatar(data.sender);
		data.when = comment_when(data.creation);
	}
}