window.user = $('#user_name').html;
window.user_list = [];
window.prev_donations = [];
window.dependencies = [];

//helper functions

/* Views for Control Group */
function showControlView(){
	$('#desc').append("Our kitty friends are so grateful for your donation. Meow, *purr* ");

	$('challenge').hide();
	$('challenges').hide();
	//Call regular visualization

	processDonation("10", "explore");
	getHighImpactPoints(10, 200);
	// regularVisualization();

}

/* Visualization for Control Group */
function regularVisualization(data, curr_donation, change){
	$('#visualization').empty();
	console.log(data);
	if(data.length < 1){
		data = [{"name": "Aysha", "donation": 10}, {"name": "Maeda", "donation": 50}, {"name": "Jay", "donation": 30}, {"name": "Juan", "donation": 100}]
	}



	var newdata = [curr_donation];
	var newchange = [];
	for(var prop in change) {
		if(change[prop] != 0 && prop != "total" && prop != window.user)
	  		newchange.push({name: prop, change: change[prop]});
	}

	var margin = {top: 20, right: 30, bottom: 30, left: 40},
	    width = $('#visualization').css('width').split("px")[0] - margin.left - margin.right,
	    height = 300 - margin.top - margin.bottom,
	    barWidth = 20;

	var y = d3.scale.linear()
	    .domain([0, 200])
	    .range([height, 0]);

	var yAxis = d3.svg.axis()
	    .scale(y)
	    .orient("left")
	    .ticks(5, "AED");

	var svg = d3.select("#visualization").append("svg")
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
	  .append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


	svg.append("g")
	  .attr("class", "y axis")
	  .call(yAxis)
	// .append("text")
	//   .attr("transform", "rotate(-90)")
	//   .attr("y", 0)
	//   .attr("dy", ".71em")
	//   .style("text-anchor", "end")
	//   // .text("Donation");

	svg.selectAll(".bars")
	      .data(data)
	    .enter().append("rect")
	      .attr("class", "bars")
	      .attr("width", barWidth - 4)
	      .attr("x", function(d, i){return margin.left + i*barWidth;})
	      .attr("y", function(d) { return y(d.donation); })
	      .attr("height", function(d) { return height - y(d.donation); })
	      .on("mouseover", function(d){ console.log(d.name);})

	if(curr_donation){
		// console.log("coming here?");
		svg.selectAll(".bars_current")
			.data(newdata)
			.enter().append("rect")
			.attr("class", "bars_current")
			.attr("width", barWidth - 4)
			.attr("x", function(d, i){
				return margin.left + data.length * barWidth; 
			})
			.attr("y", function(d){
				return y(d.donation);
			})
			.attr("height", function(d){
				return height - y(d.donation);
			})
	}
	if(newchange.length > 0){
		// console.log("coming here for new change?");
		svg.selectAll(".bars_impact")
			.data(newchange)
			.enter().append("rect")
			.attr("class", "bars_impact")
			.attr("width", barWidth - 4)
			.attr("x", function(d, i){
				return margin.left + (data.length + 1) * barWidth + i*barWidth; 
			})
			.attr("y", function(d){
				return y(d.change);
			})
			.attr("height", function(d){
				return height - y(d.change);
			})
	}


}

/* Views for Test Group */
function showTestView(){
	
	// hasDonation(window.user).done(function(){
		if(window.has_donation == true){
			//Show result


			//Call impact visualization
			regularVisualization(prev_donations);
		}
		else{
			$("<p>You can either make a direct donation or create a donation challenge that will maximize the overall donations.</p>").insertBefore($('#donation_form'));

			//Call impact visualization
			processDonation("10", "explore", "");
			getHighImpactPoints(10, 200);
		}
	// })



}


/* TODO: Visualization for Test Group */
function impactVisualization(data){

}

/* Retrieve form values and create valid donation conditions */
function getDonationCondition(condition_type, state){
  	var donation_condition = "";

  	var friends = "";
  	//FRIENDS challenge
	if(condition_type === "friendly"){
		var friend_string = "";
	  	var donation_amt = $('#friendly').children('#t1_donation_amount').val();
	  	var count = $('#friendly').find(".friendcount").length;
	  	var friend = $('#friendly').children('#friends').val();
	  	var friend_amt = $('#friendly').children('#friend_amount').val();
	  	if(friend != "" && window.user_list.indexOf(friend) > -1){
	  		friend_string = friend + " HAS " + friend_amt;
	  		friends += friend;
	  	}	



	  	if(count > 1){
	  		i = 1;
	  		while(i < count){
	  			friend = $('#friendly').children('#friends'+i).val();
	  			friend_amt = $('#friendly').children('#friend_amount'+i).val();
	  			if(friend != "" && window.user_list.indexOf(friend) > -1){
	  				friend_string += " AND " + friend + " HAS " + friend_amt;
	  				friends += "," + friend;
	  			}
	  			i++;
	  		}
	  	}

	  	if(friend_string != ""){
	  		donation_condition = donation_amt + " if " + friend_string;
	  	}
	}

	//MILESTONE challenge
	else if(condition_type === "milestone"){
		var donation_amt = $('#milestone').children('#t2_donation_amount').val();
		var total_amt = $('#milestone').children('#total_amount').val();
		donation_condition = donation_amt + " if EVERYONE HAS  " + total_amt; 
	}

	//MICRO challenge
	else if(condition_type === "micro"){
		var donation_amt = $('#micro').children('#t3_donation_amount').val();
		var num_people = $('#micro').children('#num_people').val();
		var micro_amt = $('#micro').children('#micro_amount').val();
		donation_condition = donation_amt + " if " + num_people + " PEOPLE > " + micro_amt;
	}

	console.log(donation_condition);
	console.log(friends);
	if(donation_condition != ""){

		processDonation(donation_condition, state, friends);
		
	}
}


/* Function to retrieve project statistics*/
function getProjectInfo(){
	var amt_funded = 0;
	var percent_funded = 0;
	var num_funders = 0;
	var num_challenges = 0;

	$.ajax({
		url: 'http://10.225.0.15:8000',
		method: "POST",
		data: {"action":"getProjectStats"},
		dataType: "JSON",
		success: function(response){
			console.log(response);
			amt_funded = response['amt_funded'];
			goal_amt = response['goal_amt'];
			num_funders = response['num_funders'];
			num_challenges = response['num_challenges'];

			$('#amt_funded').html(" " + amt_funded + " AED");
			$('#num_funders').html(" " + num_funders + "  ");
			$('#num_challenges').html(num_challenges + " ");

			//Update challenges
			displayChallenges();

			//Update previous donations
			prevDonations();
		},
		error: function(xhr, status, error){
			console.log("Error: " + error);
		}
	})	
}

function getRipples(){

	$.ajax({
		url: 'http://10.225.0.15:8000',
		method: "POST",
		data: {"action":"getRipples", "user": window.user, "highest": 200, "lowest": 10, "stepsize": 5},
		dataType: "JSON",
		success: function(response){
			console.log(response);
		
		},
		error: function(xhr, status, error){
			console.log("Error: " + error);
		}
	})	
}

function getNetwork(){

	$.ajax({
		url: 'http://10.225.0.15:8000',
		method: "POST",
		data: {"action":"getNetwork", "user": window.user},
		dataType: "JSON",
		success: function(response){
			console.log(response);
		
		},
		error: function(xhr, status, error){
			console.log("Error: " + error);
		}
	})	
}

/* Function to retrieve user statistics */
function getUserInfo(){
	//Get this information from the backend, based on the user that is logged in.

	//Update global variables
	window.user = "Carla";
	window.group = "test";

	$('#user_name').html(window.user);



	//Show view based on group
	if(window.group === "test"){
		showTestView();
	}
	else{
		showControlView();
	}
}



/* Function to return the last n unresolved challenges/conditions */
function displayChallenges(){
	var list = [];
	$.ajax({
		url: 'http://10.225.0.15:8000',
		method: "POST",
		data: {"action": "prevChallenges"},
		dataType: "json",
		success:function(response){
			console.log(response['challenges']);
			for(i = 0; i < response['challenges'].length; i++){

				// var partone = response['challenges'][i].split("if")[0];
				// var user = partone.split(" ")[0];
				// var amt = partone.split(" ")[1];
				// var challenge = response['challenges'][i].split("if")[1];
			
				// 	var terms = challenge.trim().split(" ");
				// 	if(terms[0] == "EVERYONE"){
				// 		console.log("milestone challenge");
				// 	}else if(terms[1] == "PEOPLE"){
				// 		console.log("micro challenge");
				// 	}else{
				// 		console.log("Friend challenge");
				// 		//Figure out the friends here.

				// 		for(j = 0; j < terms.length; j++){
				// 			if(user_list.indexOf(terms[j]) > -1){
				// 				// dependencies.push({"user": user, "target": })
				// 			}
				// 		}
				// 	}
				
				// console.log(partone);
				// var challenge = {"user" : text[0], "amt": text[1], "condition": text}
				// $('#challenges > ul').append('<li>'+ user + ' will donate ' + amt + ' IF ' + challenge + '</li>');
				$('#challenges > ul').append('<li>' + response['challenges'][i] + "</li>");
			}
		},
		error: function(xhr, status, error){
			console.log("Error: " + error);
		}
	})
}



/* Function to return the last n resolved donations */ 
function prevDonations(){
	var list = [];
	$.ajax({
		url: 'http://10.225.0.15:8000',
		method: "POST",
		data: {"action":"prevDonations", "n": 10},
		dataType: "json",
		success:function(response){
			console.log(response['donations']);
			window.prev_donations = response['donations'];
			regularVisualization(window.prev_donations);
		},
		error: function(xhr, status, error){
			console.log("Error: " + error);
		}
	})
}

/* Function that returns the highest impact donation suggestions to the user */
function getHighImpactPoints(lowest, highest){
	var list = [];
	var stepsize = 5;
	$.ajax({
		url: 'http://10.225.0.15:8000',
		method: "POST",
		data: {"action":"getHighImpactPoints","user": window.user, "lowest": lowest, "highest": highest, "stepsize": stepsize},
		dataType: "JSON",
		success:function(response){
			console.log(response['impactPoints']);
				
			$('.impact').remove();
			for(i = 0; i < response['impactPoints'].length; i++){
				console.log(response['impactPoints'][i]['amount'] + " : " + response['impactPoints'][i]['impact']);
				$('#sliders').prepend("<input type='range' class='impact' min='5' max='200' value='"+response['impactPoints'][i]['amount'] + "'></input>");
				// $('.impact').offset({'top':top + 20});
				$('.impact').attr("disabled","true");
			}

			
		},
		error: function(xhr, status, error){
			console.log("Error: " + error);
		}
	})
}

/* Function to combine the before and after values for a user */
function newDataSet(before, after){
	var newdata = [];
	 for(var prop in before, after) {
	  newdata.push({name: prop,
	     before: before[prop], after: after[prop]});
	}
   console.log(newdata);
}


/* Function to process donation */ 
function processDonation(donation_condition, state, challengees){
	console.log("challengees: " + challengees);
	$.ajax({
		url: 'http://10.225.0.15:8000',
		method: "POST",
		data: {"action":"processDonation", "user": window.user, "donation": donation_condition, "state": state, "challengees": challengees},
		dataType: "JSON",
		success: function(response){

			console.log(response);
			var total_impact = response['impact'];
			var donation_amt = donation_condition.split(" ");

			//Update values
			$('#donation_amt').val(donation_amt[0]);
			$('#your_donation').html(donation_amt[0] + " AED");
			$('#your_impact').html(parseInt(donation_amt[0]) + parseInt(total_impact) + " AED");
			$('#total_funds').html(response['after']['total'] + " AED");
			$('#curr_impact').html(parseInt(donation_amt[0]) + parseInt(total_impact)); 

			hasDonation(window.user);


			//Update the visualizations
			// if(window.group == "control"){
				var curr_donation = {"name": window.user, "donation": donation_amt[0]};
				// console.log(curr_donation);
				console.log(response['change'])
				if(prev_donations.length > 0)
					regularVisualization(prev_donations, curr_donation, response['change']);
			// }else{
				// impactVisualization(response['before'], response['after']);
			// }

		},
		error: function(xhr, status, error){
			console.log( "Error: " + error);
	        console.log( "Status: " + status );
	        console.dir( xhr );
		}
	});


	
}

// TODO: Function to check if I have been challenged
//output: {
//	list of <user, donation_challenge_amt>
//}
function checkForChallenges(){
	$.ajax({
		url: 'http://10.225.0.15:8000',
		method: "POST",
		data: {"action":"checkForChallenges", "user": window.user},
		dataType: "json",
		success: function(response){
			console.log(response['challenge']);
			for(i = 0; i < response['challenge'].length; i++){
				console.log("You were challenged by: " + response['challenge'][i]['name'] + " and the pledge was: " +  response['challenge'][i]['pledge'] );
			}

		},
		error: function(xhr, status, error){
			console.log( "Error: " + error);
	        console.log( "Status: " + status );
	        console.dir( xhr );
		}
	});

}

function afterSubmit(response){
	//Hide Donation Slider & Challenge Div
	$('#donation_form').hide();
	$('#challenge').hide();
	$('#challenges').hide();

	//Show progress of challenges.
	console.log("showing the response: " + response);
	$('#donation').append("<b><p>Thank you for your donation of " + response[2] + " AED.</p></b>")

	$('#your_donation').html(response[2]);
	$('#total_funds').html($('#amt_funded').html());
}




// TODO: Function that returns list of users in the system

function listUsers(){

	$.ajax({
		url: 'http://10.225.0.15:8000',
		method: "POST",
		data: {"action":"listUsers"},
		dataType: "json",
		success: function(response){
			window.user_list = response['users'];
			var previousValue = "";


			$('#friends').autocomplete({
			    autoFocus: true,
			    source: window.user_list,
			}).keyup(function() {
			    var isValid = false;
			    for (i in window.user_list) {
			        if (window.user_list[i].toLowerCase().match(this.value.toLowerCase())) {
			            isValid = true;
			        }
			    }
			    if (!isValid) {
			        this.value = previousValue
			    } else {
			        previousValue = this.value;
			    }
			});
			
			console.log(window.user_list);

		},
		error: function(xhr, status, error){
			console.log( "Error: " + error);
	        console.log( "Status: " + status );
	        console.dir( xhr );
		}
	});

}

/* return progress of user's donation_condition */
// function getProgress{

// }


function hasDonation(user){
	$.ajax({
		url: 'http://10.225.0.15:8000',
		method: "POST",
		data: {"action":"hasDonation", "user": user},
		dataType: "json",
		success: function(response){
			console.log(response);
			window.hasDonation == response[0];

			if(response[0] == true){
				afterSubmit(response);
			}
		},
		error: function(xhr, status, error){
			console.log( "Error: " + error);
	        console.log( "Status: " + status );
	        console.dir( xhr );
		}
	});
}

$(document).ready(function(){
	
	// //1. Load project details
	// getProjectInfo();

	// //2. Load user details and assign corresponding random view
	// // i.e get username, group (control or test), and has_donation (t/f, donation_condition, amount);
	// getUserInfo();

	// //3. Load user list for dropdown forms
	// window.user_list = [];
	// listUsers();


	// //4. Page Interactions

	//Display the appropriate challenge form
	$('.chal_form').on('click', function(){
		var curr_form = $(this).find($('.form')).attr("id");
		//Hide the other forms.
		$('.chal_form').siblings().children('.form').hide();
		//Show current form
		$('#' + curr_form).show();
	})


	//Friends Challenge - Add button interaction
	$('#addfriend').on('click', function(){

		//Count # of friends added so far
		var count = $(this).parent().find(".friendcount").length;

		//add another friend
		var formaddendum = '<input type="text" id="friends' + count + '" class="friendcount" placeholder="Add a friend"></input> also donates $<input type="number" id="friend_amount'+count+'" min="10" max="1000" value="20"></input> (optional)<br>';

		$(formaddendum).insertAfter($(this).prev());

		//Bind new form elements to appropriate interactions
		$('#friends' + count).on('input onchange', getDonationCondition("friendly"));
		$('#friend_amount' + count).on('input onchange', getDonationCondition("friendly"));

		$('#friends' + count).autocomplete({
	      source: window.user_list
	    });

	    $('#friends' + count).on('autocompleteclose', function(){
			getDonationCondition("friendly", "explore");
		})
	})


	//Function to retrieve form values and create donation condition statements
	$('.form').on('input',function(){
		var condition_type =  $(this).attr("id");
		getDonationCondition(condition_type, "explore");
	});

	$('#friends').on('autocompleteclose', function(){ 
		getDonationCondition("friendly", "explore");
	})

	//Submit donation_conditions
	$('.challenge_button').click(function(){
		var id = $(this).attr("id");
		getDonationCondition(id, "submit");
	})

	//Donation exploration
	$('#donation_amt').on("change", function() {
		var donation_amt = $(this).val()
		$('#curr_donation').html(donation_amt);
	 	processDonation(donation_amt, "explore", "");
	});

	$('#donate').click(function(){
		processDonation($('#donation_amt').val(), "submit", "");
	})
	 
	// // getRipples();
	// // checkForChallenges();
	// // regularVisualization(prev_donations, 10, [])
	// checkForChallenges();

});
