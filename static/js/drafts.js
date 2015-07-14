$(function(){
	toastr.options = {
	  "closeButton": false,
	  "debug": false,
	  "newestOnTop": false,
	  "progressBar": false,
	  "positionClass": "toast-bottom-right",
	  "preventDuplicates": false,
	  "onclick": null,
	  "showDuration": "300",
	  "hideDuration": "1000",
	  "timeOut": "2000",
	  "extendedTimeOut": "1000",
	  "showEasing": "swing",
	  "hideEasing": "linear",
	  "showMethod": "fadeIn",
	  "hideMethod": "fadeOut"
	}
	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie != '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
	var csrftoken = getCookie('csrftoken');

	$('span.star').click(function(){
		$this = $(this);
		docid = $this.parent().data('docid');
		$.ajax({
			url: '/star_document/',
			method: 'POST',
			data: {
				hashid: docid, csrfmiddlewaretoken: csrftoken,
			},
			success: function(){
				$this.toggleClass('is-starred');
				var status;
				if ($this.hasClass('is-starred')){
					status = 'starred';
				} else {
					status = 'unstarred';
				}
				toastr.success("Successfully " + status + " " + docid +"!");	
			}
		});
	});
});
