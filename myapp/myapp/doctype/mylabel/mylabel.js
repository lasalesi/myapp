// Copyright (c) 2018, lasalesi and contributors
// For license information, please see license.txt

frappe.ui.form.on('MyLabel', {
	refresh: function(frm) {
		frm.add_custom_button(__("PDF!"), function() {
			create_pdf(frm);
		}).addClass("btn-primary");
	}
	
});

function create_pdf(frm) {
	var w = window.open(
		frappe.urllib.get_full_url("/api/method/myapp.myapp.doctype.mylabel.mylabel.download_mylabel?"  
				+ "name=" + encodeURIComponent(me.frm.doc.name))
	);
	if (!w) {
		frappe.msgprint(__("Please enable pop-ups")); return;
	}
}

function download(filename, content) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:application/pdf;charset=utf-8,' + encodeURIComponent(content));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}
