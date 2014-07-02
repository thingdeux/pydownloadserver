/* Author: Josh */

function attemptQueue() {
	var returned_url = $("#addToQueueText").val();	

	if (returned_url == "")	{	
		//Make sure the queue box actually has text in it
		$("#QueueErrorBox").html('Empty URL').hide().fadeIn();
		setTimeout(function() { $("#QueueErrorBox").fadeOut(); }, 2500);
	}
	
	else {

		//Regular expression for url matching
		var regular_expression = /(^|\s)((https?:\/\/)?[\w-]+(\.[\w-]+)+\.?(:\d+)?(\/\S*)?)/gi;

		if ( returned_url.match(regular_expression) ) {
			//Post verified URL To queue handler
			var concatenated_string = "Sent:  " + returned_url + " to queue";
			$("#QueueErrorBox").html(concatenated_string).hide().fadeIn();
			setTimeout(function() { $("#QueueErrorBox").fadeOut(); }, 2500);

			$("#addToQueueText").val("");
			silentlySendDataWithPost("/addUrlToQueue", returned_url);
		}
		else
		{
			//Make sure the queue box actually has text in it
			$("#QueueErrorBox").html('Not a valid URL').hide().fadeIn();
			setTimeout(function() { $("#QueueErrorBox").fadeOut(); }, 100);		
		}

	}
}

function silentlySendDataWithPost(location, data) {
	$.post( location, data );
}

function silentlySendGet(location) {
	$.get(location);
}

//Wait for the document to load
$(document).ready(function() {
	/* --- Index Page --- */
	//Handler for queue button being clicked on index page.
	$("#addToQueueButton").click(function() {		
		attemptQueue();			
	});

	//Handler for enter being pressed after inputting url
	$("#addToQueueText").keypress(function( event ) {
			if (event.which == 13) {
				//Stop enter from doing what it normall ydoes
				event.preventDefault();
				attemptQueue();
			}
	});

	/* --- Queue Page --- */
	//var current_url = document.URL.split('/').slice(-1)[0]			

	/* --- History Page --- */
	$("#clear_history").click(function() {		
		silentlySendGet("history/delete/");
		setTimeout(function() {location.reload();}, 2500);
	})	
});


