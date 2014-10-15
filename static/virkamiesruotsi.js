$(document).ready(function(){
    $("#startquiz").click(
	function() {
		$.get("/quiz", function(data) {
			$("#quiz").html(data);
		});
    });
    $("#repeat").click(
	function() {
		$.get("/repeat", function(data) {
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
   
    $(document).on('click', '.plus',
        function() {
	        var id = $(this).attr('id');
                var $that = $(this);
		$.get("/addfavorite/"+id).done(function() {
		    $that.removeClass("plus");
	            $that.text("Lisätty")
                });
    });
    $(document).on('click', '.minus',
        function() {
	        var id = $(this).attr('id');
                var $that = $(this);
		$.get("/removefavorite/"+id).done(function() {
		    $that.removeClass("minus");
	            $that.text("Poistettu")
		});
    });

});


