/* JS file with helper functions */ 


function sanitizeString(str){
    if(/^[a-zA-Z0-9]+$/.test(str) == false) {
        alert('Input should only contain letters and numbers - no special characters.');
    }else{
        return true;
    }
}

/* Retrieves project statistics*/
function getProjectInfo(){
    $.ajax({
         url: 'http://127.0.0.1:8080/rippler',
        method: "POST",
        data: {"action":"getProjectStats"},
        dataType: "JSON",
        success: function(response){
            // console.log(response);

            $('#amt_funded > .big_num').html("  " + Math.floor(response['amt_funded']) + " AED");
            $('#num_funders > .big_num').html(" " + response['num_funders'] + "  ");
            $('#num_challenges > .big_num').html(response['num_challenges'] + " ");
            prevDonations();
        },
        error: function(xhr, status, error){
            console.log("Error in getProjectInfo  method: " + error);
        }
    })  
}

/* Returns the last n resolved donations */ 
function prevDonations(){
    $.ajax({
        url: 'http://127.0.0.1:8080/rippler',
        method: "POST",
        data: {"action":"prevDonations", "n": 1000},
        dataType: "json",
        success:function(response){
            donations = response['donations'];
            prevChallenges();
            if(window.has_donation){
                afterSubmit(window.donation_condition, window.donation_amt);
            }

        },
        error: function(xhr, status, error){
            console.log("Error in prevDonations: " + error);
        }
    })
}

/* Returns unresolved donation challenges */
function prevChallenges(){
    var list = [];
    $.ajax({
        url: 'http://127.0.0.1:8080/rippler',
        method: "POST",
        data: {"action": "prevChallenges"},
        dataType: "json",
        success:function(response){
            // console.log(response['challenges']);
            challenges = response['challenges'];
            
            // console.log(window.user);
            if(window.user){
                checkForChallenges();
                getChallengesForAmount(window.user, 20);
            }
            else{
                // console.log("not logged in");
                getPublicChallenges();

            }
        },
        error: function(xhr, status, error){
            console.log("Error in Challenges: " + error);
        }
    })
}
/* FOCUS ON THIS */
/* Processes a donation_condition in the "explore" or "submit" states */ 
function processDonation(donation_condition, state, challengees){
    console.log(donation_condition);
    $.ajax({
        url: 'http://127.0.0.1:8080/rippler',
        method: "POST",
        data: {"action":"processDonation", "user": window.user, "donation": donation_condition, "state": state, "challengees": challengees, "system": system},
        dataType: "JSON",
        success: function(response){
            // console.log(state);
            // console.log(response);
            var total_impact = response['impact'];
            var donation_amt = donation_condition.split(" ");

            //Update values
            $('#donation_amt').val(donation_amt[0]);
            $('#your_donation').html(parseInt(donation_amt[0]) + " AED");


            curr_donation = {"name": window.user, "donation": donation_amt[0], "condition": donation_condition, "challengees": challengees};

            // if(donations.length > 0)
            //     regularVisualization(donations, curr_donation, response['change']);

            getChallengesForAmount(user, parseInt(donation_amt[0]));
            if(state == "submit"){
                getProjectInfo();
                survey(donation_condition, parseInt(donation_amt[0]));
                window.donation_condition = donation_condition;
                window.donation_amt = parseInt(donation_amt[0]);
                // afterSubmit(donation_condition, parseInt(donation_amt[0]));
            }

        },
        error: function(xhr, status, error){
            console.log( "Error: " + error);
            console.log( "Status: " + status );
            console.dir( xhr );
        }
    }); 
}

/* Returns list of challenges for the user */
function checkForChallenges(){
    $.ajax({
        url: 'http://127.0.0.1:8080/rippler',
        method: "POST",
        data: {"action":"checkForChallenges", "user": window.user},
        dataType: "json",
        success: function(response){
            // console.log("You've been challenged " + response['challenge'].length +  " times.");

            notifications = response['challenge'];

            if(response['challenge'].length == 0){
                $('#notifications').hide();
            }

            if(!window.has_donation)
                $('#noti').html("<div class='title'>You've been challenged!</div>")
            var noti_text = "<div id='noti_text'><br><ul>"
            for(var i = 0; i < response['challenge'].length; i++){
                // <b>" + response['challenge'][i]['name'] + "</b> mentioned you in a pledge:  <em>" + 
                noti_text += "<li> " + nlCondition(response['challenge'][i]['name'] + " " + response['challenge'][i]['pledge']) + "</em></li>";
            }

            noti_text += "</ul></div>";
            $("#noti").append(noti_text);

        },
        error: function(xhr, status, error){
            console.log( "Error: " + error);
            console.log( "Status: " + status );
            console.dir( xhr );
        }
    });
}

/* Returns a user's donation amount */
function getUserDonation(user){
    for(var i = 0; i < donations.length; i++){
        if(donations[i]['name'].toLowerCase() == user.toLowerCase()){
            return donations[i]['donation'];
        }
    }
    return 0;
}

/* Returns a user's challenge */
function getUserChallenge(user){

    for(var i = 0; i < challenges.length; i++){
        if(challenges[i].split(" ")[0] == user){
            return challenges[i]
        }
    }
    return "";
}

/* Returns a user's challenge(s) for a certain amount */
function getChallengesForAmount(user, amount){   
    var count = 0; 
    var triggers =[];
    for(var i = 0; i < challenges.length; i++){
        // console.log(challenges[i]);
        var terms = challenges[i].split(" ");
        if(terms.indexOf(user) > -1){
            count++;
            //check if other users are present in this challenge
            var num_people = 0;
            var progress = 0;
            var friend; 
            var ch_amount = 0;
            for(b=0; b<terms.length;b++){
                if(terms[b] == "HAS"){
                    num_people++;
                    friend = terms[b-1];

                    if(friend != window.user){
                        if(getUserDonation(friend) >= parseInt(terms[b+1])){
                            progress++;
                        }
                    }
                    ch_amount = terms[b+2];
                }
            }


            if(parseInt(ch_amount) <= amount){
                triggers.push({"challenge": nlCondition(challenges[i]), "progress": progress, "num_people": num_people,"needed": num_people - progress});
            }

        }
        else if(terms.indexOf("PEOPLE") > -1){
            var ind = terms.indexOf("PEOPLE");
            if(parseInt(terms[ind+2]) <= amount){
                var ch_amount = parseInt(terms[ind+2]);
                var num_people = parseInt(terms[ind-1]);
                var progress = microProgress(parseInt(ch_amount));
                var percent = Math.floor((progress/num_people)*100);
                triggers.push({"challenge": nlCondition(challenges[i]), "progress": progress, "num_people": num_people, "needed": num_people - progress});
                count++;
        
            }
        }
    }
    /* Displaying challenges ordered by percentage completed */
    triggers.sort(function(a, b){return a.needed - b.needed});

    $('#trigger_table').empty();
    // console.log(triggers);
    var list = "<ul>";
    
    for(var a in triggers){
        var logodiv = "<img src='static/img/lock.png' class='icon-small'>";
        var unlocked = "locked", color = "";
        if(triggers[a].needed == 1){
            unlocked = "unlocked";
            logodiv = "<img src='static/img/unlock.png' class='icon-small'>";
            list += "<li><div class='item'><div style='width: 70%; float: left; padding-bottom: 10px; '>" + logodiv + triggers[a].challenge + "</div><div style='width: 25%; float: right;'><div class='circle " + unlocked + "'><b>     YOU</b></div></div></div></li>"
        }else{
            list += "<li><div class='item'><div style='width: 70%; float: left; padding-bottom: 10px; '>" + logodiv + triggers[a].challenge + "</div><div style='width: 25%; float: right;'><div class='circle " + unlocked + "'><b>" +  triggers[a].needed + "</b><br>more</div></div></div></li>"
        }
    }
    list += "</ul>";
     
    if(count > 0){
        $('#trigger_list').empty();
        $('#trigger_list').append(list);
        $('#triggers').show();
    }else{
        $('#triggers').hide();
    }
}

/* Returns a user's challenge(s) for a certain amount */
function getPublicChallenges(){   
    var count = 0; 
    var triggers =[];
    for(var i = 0; i < challenges.length; i++){
        // console.log(challenges[i]);
        var terms = challenges[i].split(" ");
    
        if(terms.indexOf("PEOPLE") > -1){
            var ind = terms.indexOf("PEOPLE");
            var ch_amount = parseInt(terms[ind+2]);
            var num_people = parseInt(terms[ind-1]);
            var progress = microProgress(parseInt(ch_amount));
            var percent = Math.floor((progress/num_people)*100);
            // terms.splice(0, 1);
            // var public_chall = "Someone " + terms.join().replace(/,/g, ' ');
            // console.log(public_chall);
            triggers.push({"challenge": nlCondition(challenges[i]), "progress": progress, "num_people": num_people, "needed": num_people - progress});
            count++;
        
            
        }
        else{
            var num_people = 0;
            var progress = 0;
            var friend; 
            var ch_amount = 0;
            for(b=0; b<terms.length;b++){
                if(terms[b] == "HAS"){
                    num_people++;
                    friend = terms[b-1];
                    // console.log(friend);
                    // console.log(terms[b+2]);
                    if(getUserDonation(friend) >= parseInt(terms[2+b])){
                        progress++;
                    }
                    // console.log(progress);
               
                    ch_amount = terms[b+2];
                }
            }
            
            triggers.push({"challenge": nlCondition(challenges[i]), "progress": progress, "num_people": num_people,"needed": num_people - progress});
            
        }
    }
    /* Displaying challenges ordered by percentage completed */
    triggers.sort(function(a, b){return a.needed - b.needed});

    $('#trigger_table').empty();
    // console.log(triggers);
    var list = "<ul>";
    
    for(var a in triggers){
        var logodiv = "<img src='http://10.225.0.15:8000/static/img/lock.png' class='icon-small'>";
        var unlocked = "locked", color = "";
        list += "<li><div class='item'><div style='width: 70%; float: left; padding-bottom: 10px; '>" + logodiv + triggers[a].challenge + "</div><div style='width: 25%; float: right;'><div class='circle " + unlocked + "'><b>" +  triggers[a].needed + "</b><br>more</div></div></div></li>"

    }
    list += "</ul>";
     
    if(count > 0){
        $('#trigger_list').empty();
        $('#trigger_list').append(list);
        $('#triggers').show();
    }else{
        $('#triggers').hide();
    }
}

/* Returns the number of people who have donated at least a certain amount */
function microProgress(amt){

    var count = 0;
    var l = 0;

    for(var l=0; l < donations.length; l++){
        if(donations[l]['donation'] >= amt){
            count++;
        }
    }
   
    return count; 
}

/* Returns the donation challenge condition in a natural language form */
function nlCondition(donation_condition){
    console.log(donation_condition);
    var terms = donation_condition.split(" ");
    var donation_amt = terms[1]; 
    var micro_amt = 0;
    var num_people = 0; 
    var mile_amt = 0;
    var node = terms[0];


    if(terms.indexOf('EVERYONE') > -1){
        //milestone
        mile_amt = terms[terms.length - 1];
        return "<b>" + node + "</b> will donate <b>" + donation_amt + " AED</b> if the total amount hits " + mile_amt + " AED.";
    }
    else if(terms.indexOf('PEOPLE') > -1){
        num_people = terms[terms.indexOf('IF') + 1];
        micro_amt = terms[terms.length - 1];
        return "<b>" + node + "</b> will donate <b>" + donation_amt + " AED</b> if " + num_people + " people donate at least " + micro_amt + " AED.";
    }       
    else{
        condition = donation_condition.split("IF")[1];
        var friend_string = "";
        var friends = [];
        var count = 0;
        for(var j = 0; j < terms.length; j++){
            if(terms[j] == "HAS"){
                count++;
                if(count < 2){
                    friend_string += "if <b>" + terms[j-1] + "</b> donates at least <b>" + terms[j+2] + " AED</b>" 
                    friends.push(terms[j-1]);

                }else{
                    friend_string += " and if <b>" + terms[j-1] + "</b> donates at least <b>" + terms[j+2] + " AED</b>"
                    friends.push(terms[j-1]); 
                }

            }
        }
        return "<b>" + node + "</b> will donate <b>" + donation_amt + " AED</b> " + friend_string  + ".";
  
    }
}

function checkFriend(name){
    for(var a in donations){
        if (donations[a].name.toLowerCase() == name){
            return true;
        }
    }

    for (var b in challenges){
        if (challenges[b].split(" ")[0].toLowerCase() == name){
            return true;
        }
    }

    return false;
}

/* Retrieves form values and creates valid donation conditions */
function getDonationCondition(condition_type, state){
    var donation_condition = "";

    var friends = "";
    //FRIENDS challenge
    if(condition_type === "friendly"){
        $('#current_friends').empty();
        var friend_string = "";
        var donation_amt = $('#friendly').children('#t1_donation_amount').val();
        var count = $('#friendly').find(".friendcount").length;
        var friend = $('#friendly').children('#friends').val();
        

        // console.log("why no work?");
        var friend_amt = $('#friendly').children('#friend_amount').val();
        if(friend_amt.toString().indexOf('.') > -1){
            friend_amt = Math.floor(friend_amt);
        }

        if(friend != "" && sanitizeString(friend)){
            friend_string = friend + " HAS > " + friend_amt;
            friends += friend;
            if(friend == window.user){
                $('#current_friends').html("You cannot challenge yourself. Sorry!<br>");
                $('#current_friends').show();                
                return false;
            }
            //Check if friend has already donated.
            // console.log(checkFriend(friend.toLowerCase()))
            if(checkFriend(friend.toLowerCase())){
                var much = getUserDonation(friend);
                if(much < friend_amt){
                    $('#current_friends').html("<b>" + friend + "</b> has already donated an amount that does not meet your challenge. <br>");
                    $('#current_friends').show();                
                    return false;
                }
            }
        }   

        if(count > 1){
            i = 1;
            while(i < count){
                friend = $('#friends'+i).val();
                friend_amt = $('#friend_amount'+i).val();
                // console.log(friend);
                // console.log(friend_amt);
                if(friend_amt.toString().indexOf('.') > -1){
                    friend_amt = Math.floor(friend_amt);
                }

                if(friend != "" && sanitizeString(friend)){
                    friend_string += " AND " + friend + " HAS > " + friend_amt;
                    friends += "," + friend;

                    if(friend == window.user){
                        $('#current_friends').html("You cannot challenge yourself. Sorry!<br>");
                        $('#current_friends').show();                
                        return false;
                    }
                    // console.log(checkFriend(friend));
                    if(checkFriend(friend)){
                        var much = getUserDonation(friend);
                        if(much < friend_amount){
                            $('#current_friends').html("<b>" + friend + "</b> has already donated an amount that does not meet your challenge. <br>");
                            $('#current_friends').show();                
                            return false;
                        }
                    }
                }
                i++;
            }
        }

        if(friend_string != ""){
            donation_condition = donation_amt + " IF " + friend_string;
        }
    }

    //MILESTONE challenge
    else if(condition_type === "milestone"){
        var donation_amt = $('#milestone').children('#t2_donation_amount').val();
        var total_amt = $('#milestone').children('#total_amount').val();
        donation_condition = donation_amt + " IF EVERYONE HAS > " + total_amt; 
    }

    //MICRO challenge
    else if(condition_type === "micro"){
        var donation_amt = $('#micro').children('#t3_donation_amount').val();
        var num_people = $('#micro').children('#num_people').val();
        if(num_people.toString().indexOf('.') > -1){
            num_people = Math.floor(num_people);
        }
        var micro_amt = $('#micro').children('#micro_amount').val();
        if(micro_amt.toString().indexOf('.') > -1){
            micro_amt = Math.floor(micro_amt);
        }

        // console.log(micro_amt);

        var micro_progress = microProgress(micro_amt);

        $('#current_stats').html("There are currently " + micro_progress + " people who satisfy your challenge!") 
        $('#current_stats').show();

        donation_condition = donation_amt + " IF " + num_people + " PEOPLE > " + micro_amt;
  
    }

    console.log(donation_condition);
    // console.log(friends); 

    if(donation_condition != "")
        processDonation(donation_condition, state, friends);
}



/* Processes screen after a donation is submitted */
function afterSubmit(donation_condition, donation){
    
    //Hide Donation Slider & Challenge Div
    $('#donation').remove();
    $('#challenge').remove();
    $('#notifications').remove();
    // $('#notifications').replaceWith("<div id='thankyou' class='container'></div>");

    $('#thankyou > .container').empty();
    $('#thankyou > .container').append("<h3>THANK YOU, " + user +"!</h3>" +
                                        "<p><b>If the campaign resolves, we will contact you with details regarding donation collection.</b></p>");

    var pledge = nlCondition("I" + " " + donation_condition);
    $('#thankyou > .container').append("<div class='row boxes'><div class='pledge one-half column' ><h5 class='title'>MY PLEDGE</h5><div class='pledge_box'>" + 
                                            pledge + " </div><br><p>Sincerely,<br> "+ user +" </p></div></div>");


    //IF direct donation
    var success = 0;
    // console.log(donation_condition.indexOf('IF'));
    if(donation_condition.indexOf('IF') <= -1){
        // console.log("should be here");
        $('#thankyou > .container').append("<div style='clear: both;'><br><h5 class='title>PLEDGE AMOUNT: " + donation + " AED. </h5></div>");
        success = 1;
    }
    else{

        if(donation_condition.indexOf('EVERYONE') > -1){
            var challenge_amt = donation_condition.split(" ")[5];
            var total = $('#amt_funded > .big_num').html();
             if(total > challenge_amt){
                console.log("success");
            }
            $('#thankyou > .container > .boxes').append("<div class='progress one-half column'><h6>CHALLENGE PROGRESS</h6><table><tr>Your challenge: " + challenge_amt + " <tr>" + 
                "<tr>Amount Raised: " + total + " <tr></table></div>");
        }
        else if(donation_condition.indexOf('PEOPLE') > -1){
            var micro_amt = donation_condition.split(" ")[5];
            var num_people = donation_condition.split(" ")[2];
            var met_challenge = microProgress(micro_amt);
            if(microProgress(micro_amt) >= parseInt(num_people)){
                success = 1;
                // console.log("success");
            }
            $('#thankyou > .container > .boxes').append("<div class='progress one-half column'><h6>CHALLENGE PROGRESS</h6><table><tr><td>You challenged " + num_people + " people to donate " + micro_amt +
             " AED </td></tr><tr><td>Progress: <b>" + met_challenge + " / " + num_people  + "</b> </td></tr></table></div>");

        }
        else{

            var friends = [];
            var terms = donation_condition.split(" ")
             // $('#thankyou > .container').append("<div class='progress'><table>Table created</table></div>");

            var table = "<div class='progress one-half column'><h6>CHALLENGE PROGRESS</h6> <table><tr class='highlight'><td>Friend</td><td>Donation</td></tr>";
            for(var ind = 0; ind < terms.length; ind++){

                if(terms[ind] == "HAS"){
              
                    var name = terms[ind-1];
                    var don = terms[ind+2];
                    var actual_donation = getUserDonation(name);
    
                    table += "<tr><td>"+ name + "</td><td> " + actual_donation + " AED</td></tr>";
                    if(actual_donation >= don){
                        success = 1;
                    }

                }
            }
            table += "</table></div>";
             $('#thankyou > .container > .boxes').append(table);
        }
    }

    // if((success == 1 && system == "test") || system == "control"){
    //     $('#thankyou').append("<div class='u-cf'><br><h5 class='title'>PLEDGE AMOUNT: " + donation + " AED</h5></div><div><h5 class='title'>STATUS: COMPLETED</h5></div>");
    // }
    // else if(success == 0 && system=="test"){
    //      $('#thankyou').append("<div class='u-cf'><br><h5 class='title'>STATUS: PENDING</h5></div>");
    // }   
    // $('#thankyou').append("<div style='clear: both;'>Multiply your impact, share this campaign with your friends. Also, please fill out our survey: link</div><hr>");
}



