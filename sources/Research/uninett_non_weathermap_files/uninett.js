$(document).ready(function(){

	// Back button
	$("#back-button").click(function () { 
      history.back();
	  return false;
    });
	


	$(".node-form .standard fieldset.collapsible").addClass('collapsed');
	//$(".hierarchical-select .selects .form-select").css("height","250px");

	/*$(".view-bildegalleri .item-list").jCarouselLite({
		btnNext: ".next",
		btnPrev: ".prev",
		visible: 5,
		circular: false,
		mouseWheel: true
	});*/
	// Finds the nid of the first image in the gallery
	//var path = $(".views-row-first").find(".image-nid").text();	
	 
	// Loads the the image with the class -first to prevent it from showing
	// nothing when we first enter the gallery
	// var first = $(".views-row-first").find(".image-nid").text();
	// $("#placeholder").load("http://brave.uninett.no/fas/node/" + first + "/component")	
	// $("#node-"+first).addClass('active');

	// When a thumbnail is clicked it will load the full sized image using ajax
	$(".bilde-teaser").livequery('click', function() {
	//$(".bilde-teaser").click(function () { 	
		//finner nid
		//var path = $(this).find(".image-nid").text();
		var toLoad = $(this).find("a").attr("href") + "/component";
		$(".bilde-teaser").removeClass('active');
		$('#placeholder').animate({opacity: 0.0}, 1, loadContent);
		$('#load').remove();
		$('#fullvisning').append('<div id="load"></div>');
		$('#load').fadeIn('normal');
		function loadContent() {
			$('#placeholder').load(toLoad, showNewContent);
		}
		function showNewContent() {
			var nid = $('.bilde-full').find(".image-nid").text();
			$("#node-"+nid).addClass('active');
			$('#load').fadeOut('normal');
			$('#placeholder').animate({opacity: 1.0}, 500);
		}
		//$("#placeholder").load("http://server2.nymedia.no/uninett/node/" + path)
		//$('#placeholder').load(toLoad)
		//alert(toLoad);
		return false;
	});

	// When you hover your mouse pointer over a thumbnail it will fade down to
	// 0.5 opacity and when you take it away it will fade back to normal
	$(".bilde-teaser img") 
		.livequery(function(){ 
		// Use the helper function hover to bind a mouseover and mouseout event 
			$(this) 
				.hover(function() { 
					$(this).css({opacity: 1.0})
				}, function() { 
					$(this).fadeTo("normal", 0.5);
				}); 
		}, function() { 
			// Unbind the mouseover and mouseout events 
			$(this) 
				.unbind('mouseover') 
				.unbind('mouseout'); 
		}); 
});