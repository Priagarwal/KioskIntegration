/*
function process() {
  var html;
  var template = $('#template').val();
  eval( $('#data').val() );
  html = Mustache.render( template, data );
  $('#html').text( html );
 $('#result').html( html );

 }

*/
function process() {
                    var request1 = $.ajax({
                        url: "./checkedIn.js",
                        type: "GET"
                    });
 
                    request1.done(function() {
						console.log('request done');
						var html;
						var template = $('#template').val();
						eval( $('#data').val() );
						html = Mustache.render( template, data );
						$('#html').text( html );
						$('#result').html( html );
						eval( $('#recognized').val() );
						$('#current_user').html(recognized.identifiedPerson);
						
                    });
 
                    request1.fail(function(jqXHR, textStatus) {
						console.log('request failed');
                        alert( "Request failed: " + textStatus );
						console.log(jqXHR);
                    });
					var request2 = $.ajax({
                        url: "./recognized.js",
                        type: "GET"
                    });
 
                    request2.done(function() {
						console.log('request done');
						eval( $('#recognized').val() );
						$('#current_user').html(recognized.identifiedPerson);
						
                    });
 
                    request2.fail(function(jqXHR, textStatus) {
						console.log('request failed');
                        alert( "Request failed: " + textStatus );
						console.log(jqXHR);
                    });
					var request3 = $.ajax({
                        url: "capture.jpg",
                        type: "GET"
                    });
 
                    request3.done(function() {
						$('#imgButton').html( "capture.jpg" );						
                    });
 
                    request3.fail(function(jqXHR, textStatus) {
						console.log('request failed');
                        alert( "Request failed: " + textStatus );
						console.log(jqXHR);
                    });
					setTimeout(process, 2000); 
                }
				
