var main_module = {
	open_modal : function(url,is_large) {
		// Open Modal
		
		if(is_large){
			$("#main_modal .modal-dialog").addClass('modal-lg')
		}
		else{
			$("#main_modal .modal-dialog").removeClass('modal-lg')
		}
		
		$("#main_modal .modal-content").load(url,
				function(response, status, xhr) {
					if (status != "error") {
						$("#main_modal").modal('show');
					}
				});
	},
	close_modal : function() {
		$("#main_modal").modal('hide');
		setTimeout(function() {
			$("#main_modal .modal-content").html('')
		}, 500);
	},
	set_active_menu_item: function(url){
		$('.metismenu').find('li').removeClass('active');

		$('a[href="'+url+'"]').parents("li").addClass('active');
		$('a[href="'+url+'"]').parents("ul.nav-second-level").addClass('in');
	},
}