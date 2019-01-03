function copy_token() {
	var token = document.getElementById("token");
	token.select();
	document.execCommand("copy");

	$('#token-alert').removeClass('hidden');
}

$('.js-reset-token-form').on('submit', function (e) {
	e.preventDefault();
	var theForm = $(this);
	var token_show = $('#token');
	var token_input = $('#token-input');
	var token_error = $('#token-error');

	$.ajax({
		type: 'POST',
		url: theForm.attr('action'),
		data: $(theForm).serialize(),
		success: function (data) {

			if (data.success) {
				token_show.val(data.token);
				token_input.val(data.token);

			} else if (!data.success) {
				token_error.removeClass('hidden')
			}
		}
	});
});
