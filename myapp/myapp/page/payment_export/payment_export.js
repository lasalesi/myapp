frappe.pages['payment_export'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __('Payment Export'),
		single_column: true
	});

	frappe.payment_export.make(page);
	frappe.payment_export.run(page);
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
			
            download("payments.xml", "<xml><payment><iban>123456</iban></payment></xml>");

		});
	},
	run: function(page) {  
		// populate payment entries
		frappe.call({
			method: 'myapp.myapp.page.payment_export.payment_export.get_payments',
			args: { },
			callback: function(r) {
				if (r.message) {
					var parent = page.main.find(".payment-table").empty();
                    $('<table>').appendTo(parent);
					for (var i = 0; i < r.message.payments.length; i++) {
						$('<tr><td>' + r.message.payments[i] + '</td></tr>').appendTo(parent);
					}
                    $('</table>').appendTo(parent);
				} 
			}
		});
	}
}

function download(filename, content) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}
