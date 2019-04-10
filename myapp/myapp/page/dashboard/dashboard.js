frappe.pages['dashboard'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Dashboard',
		single_column: true
	});

    
	wrapper = $(wrapper).find('.layout-main-section');
	wrapper.append(`
			<div id="chart"></div>
		`);

	const chart_data = {
		labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
		datasets: [
			{
                name: __("Revenue PY"), 
                chartType: 'line',
				values: ['0','10','20','30','40','50','60','70','50','40','30','20']
			}
		]
	};
    
	const graph = new Chart( "#chart", {
		data: chart_data,
		type: 'line'
	});

	setTimeout(function () { graph.draw(!0); }, 1);

}
