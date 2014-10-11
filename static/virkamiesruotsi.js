$(document).ready(function(){
    $("#startquiz").click(
	function() {
		$.get("/quiz", function(data) {
			$("#quiz").html(data);
		});
    });

    $(document).on('click', '#evaluate', 
	function() {
		var $allInputs = $(".user_input"); 
		var values = {};
		$allInputs.each(function() {
			var value =  $(this).val();
			var id =  $(this).attr("id");
			values[id] = value;
		});

		$.post("/quiz", values).done(function(data) {
			$("#quiz").html(data);
		});
    });
});


