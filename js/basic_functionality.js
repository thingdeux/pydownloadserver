function attemptQueue() {
	var returned_url = $("#addToQueueText").val();
		
	if (returned_url == "")	{
		$("#QueueErrorBox").html("Empty URL")
	}
	else {
		var concatenated_string = "Queueing: " + returned_url;
		$("#QueueErrorBox").html(concatenated_string);
		$("#addToQueueText").val("");
		silentlySendDataWithPost("/addUrlToQueue", returned_url);		
	}
}

function silentlySendDataWithPost(location, data)
{
	$.post( location, data );
}


//Wait for the document to load --- write everything in here
$(document).ready(function() {
	
	// --- Index Page --- //
	//Handler for queue button being clicked on index page.
	$("#addToQueueButton").click(function() {
		attemptQueue();			
	});

	//Handler for enter being pressed after inputting url
	$("#addToQueueText").keypress(function( event ){
			if (event.which == 13)
			{
				//Stop enter from doing what it normally does
				event.preventDefault();
				attemptQueue();
			}
	});

	// --- Queue Page --- //

});


