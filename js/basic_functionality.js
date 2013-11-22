function attemptQueue()
{
	var returned_url = $("#addToQueueText").val();
		
	if (returned_url == "")
	{
		$("#QueueErrorBox").html("Empty URL")
	}
	else
	{
		var concatenated_string = "Queueing: " + returned_url;
		$("#QueueErrorBox").html(concatenated_string);
	}
}


//Wait for the document to load
$(document).ready(function(){
	
	//Handler for queue button being clicked.
	$("#addToQueueButton").click(function(){
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

});


