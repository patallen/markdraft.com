$(document).ready(function() {
	var loadToPreview = function(){
	  	$('#md-preview').html(marked($('#md-input').val()))
	};
	var highlightCode = function(){
		$('pre code').each(function(i, block){
			hljs.highlightBlock(block);
		});
	};
	loadToPreview();
	highlightCode();
	$('#md-input').keyup(function(){
		loadToPreview();
		highlightCode();
	});

	$('#editor-save').click(function(){
		$('#editor-form').submit();
	});

	$('#drawer-tab').click(function(){
		$(this).parent().toggleClass('active');
	});
});
