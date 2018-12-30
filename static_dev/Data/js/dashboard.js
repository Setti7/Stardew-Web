
$("#more-stats-btn").click(function () {
	$('html,body').animate({
			scrollTop: $("#more-stats").offset().top
		},
		'slow');
});

$(document).ready(function () {
	$('[data-toggle="tooltip"]').tooltip();
});

$(document).ready(function () {
	$('.delete-data-form').on('submit', function (e) {
		e.preventDefault();
		var theForm = $(this);
		$.ajax({
			type: 'POST',
			url: '{% url "api data delete" %}',
			data: $(theForm).serialize(),
			success: function () {
				theForm.parents('tr').fadeOut();
				$("#user-score-div").load(location.href + " #user-score-div");
				$("#hall-of-fame").load(location.href + " #hall-of-fame");
				$("#help-percent-header").load(location.href + " #help-percent-header");
			}
		});
	});

});