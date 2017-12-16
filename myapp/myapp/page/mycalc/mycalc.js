frappe.pages['mycalc'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __('MyCalc'),
		single_column: true
	});

	frappe.mycalc.make(page);
	// frappe.mycalc.run();
	//this.make_upload();
}

frappe.mycalc = {
	start: 0,
	make: function(page) {
		var me = frappe.mycalc;
		me.page = page;
		me.body = $('<div></div>').appendTo(me.page.main);
		// me.body = $('<div></div>' + '<h1>Hello World!</h1>').appendTo(me.page.main);
		var data = "MyCalc";
		$(frappe.render_template('mycalc', data)).appendTo(me.body);

		/* me.more = $('<div class="for-more"><button class="btn btn-sm btn-default btn-more">'
			+ __("More") + '</button></div>').appendTo(me.page.main)
			.find('.btn-more').on('click', function() {
				me.start += 40;
				me.run();
			}); */

		// attach button handlers
		this.page.main.find(".btn-calc-volume").on('click', function() {
			// get values from html form
			var source_volume = $('#source_volume').val();
			var source_volume_uom = $('#source_volume_uom').val();
			var destination_volume_uom = $('#destination_volume_uom').val();

			window.alert(source_volume + " " + source_volume_uom + " --> ? " + destination_volume_uom); 

			// set calculation result
			var destination_volume = frappe.mycalc.calculate_volume(source_volume, 
				source_volume_uom, destination_volume_uom);
			$('#destination_volume').val(destination_volume);
		});
		this.page.main.find(".btn-insert-log").on('click', function() {
			var me = frappe.mycalc;
			var comment = $('#comment').val();
			frappe.call({
				method: 'myapp.myapp.page.mycalc.mycalc.insert_log',
				args: {
					comment: comment
				},
				callback: function(r) {
					if(r.message) {
						/*this.page.main.find(".insert-log").removeClass("hide");
						var parent = this.page.main.find(".insert-log-messages").empty();
						$('<p>Logged!</p>').appendTo(parent);*/
						window.alert("done");
					} 
				}
			});
		});
	},
	run: function() {
		var me = frappe.mycalc;
		frappe.call({
			method: 'myapp.mycalc.get_data',
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
		var me = frappe.mycalc;

		data.by = frappe.user.full_name(data.sender);
		data.avatar = frappe.avatar(data.sender);
		data.when = comment_when(data.creation);
	},
	calculate_volume: function(source_value, source_uom, destination_uom) {
		// norm value to L
		var normed_value = source_value;
		if (source_uom == "cm3") {
			normed_value = source_value / 1000;
		}
		else if (source_uom == "m3") {
			normed_value = source_value * 1000;
		}

		// compute destination
		var destination_value = normed_value;
		if (destination_uom == "m3") {
			destination_value = normed_value / 1000;
		}
		else if (destination_uom == "cm3") {
			destination_value = normed_value * 1000;
		}

		return destination_value;
	}
}