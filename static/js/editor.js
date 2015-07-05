$(document).ready(function() {
	var loadToPreview = function(){
	  	$('#md-preview').html(marked($('#md-input').val()))
	};
	var highlightCode = function(){
		$('pre code').each(function(block) {
	    	hljs.highlightBlock(block);
	  	});
	};
	loadToPreview()
	$('#md-input').keyup(function(){
		highlightCode();
		loadToPreview();
	});
});


	