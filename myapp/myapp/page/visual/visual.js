frappe.pages['visual'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __('Visual'),
		single_column: true
	});

	frappe.visual.make(page);
	// frappe.visual.run();

	/* if(frappe.model.can_read('Daily Work Summary Settings')) {
		page.add_menu_item(__('Daily Work Summary Settings'), function() {
			frappe.set_route('Form', 'Daily Work Summary Settings');
		});
	} */
}

frappe.visual = {
	start: 0,
	make: function(page) {
		var me = frappe.visual;
		me.page = page;
		me.body = $('<div></div>'
			+ '<h1>Hello World!</h1>').appendTo(me.page.main);
		var data = "Hello World!";
		$(frappe.render_template('visual_template', data)).appendTo(me.body);
		me.more = $('<div class="for-more"><button class="btn btn-sm btn-default btn-more">'
			+ __("More") + '</button></div>').appendTo(me.page.main)
			.find('.btn-more').on('click', function() {
				me.start += 40;
				me.run();
			});
	},
	run: function() {
		var me = frappe.visual;
		frappe.call({
			method: 'myapp.visual.get_data',
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
		var me = frappe.visual;

		data.by = frappe.user.full_name(data.sender);
		data.avatar = frappe.avatar(data.sender);
		data.when = comment_when(data.creation);

		var date = frappe.datetime.str_to_obj(data.creation);
		var last = me.last_feed_date;

		if((last && frappe.datetime.obj_to_str(last) != frappe.datetime.obj_to_str(date)) || (!last)) {
			var diff = frappe.datetime.get_day_diff(frappe.datetime.get_today(), frappe.datetime.obj_to_str(date));
			var pdate;
			if(diff < 1) {
				pdate = 'Today';
			} else if(diff < 2) {
				pdate = 'Yesterday';
			} else {
				pdate = frappe.datetime.global_date_format(date);
			}
			data.date_sep = pdate;
			data.date_class = pdate=='Today' ? "date-indicator blue" : "date-indicator";
		} else {
			data.date_sep = null;
			data.date_class = "";
		}
		me.last_feed_date = date;

		$(frappe.render_template('team_update_row', data)).appendTo(me.body)
	}
}
