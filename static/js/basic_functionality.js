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

		if ( returned_url.match(regular_expression) )
		{
			//If so send whatever text it happens to be to the queue handler
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
			setTimeout(function() { $("#QueueErrorBox").fadeOut(); }, 2500);		
		}

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


