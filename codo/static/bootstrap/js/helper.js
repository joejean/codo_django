/* JS file with helper functions */ 
var baseUrl = window.djangoData['baseUrl'];
var user = window.djangoData['user_email']; //Here user is email of the user
var campaign = window.djangoData['campaign'];
var has_donation = window.djangoData['has_donation'];
var donation_condition = window.djangoData['donation_condition'];
var donation_amt = window.djangoData['donation_amt'];
var csrftoken = Cookies.get('csrftoken');

//TODO: CHANGE THIS BACK TO NORMAL
function sanitizeString(str){
    //Make sure the string is an email.
    var re = /^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
    if(re.test(str) == false) {
        return true;
        //alert('You should Provide a valid Email Address');
    }else{
        return true;
    }
}

/*The following CSRF related stuff is for Django to work otherwise
we get a forbidden error */
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

/* Retrieves project statistics*/
function getProjectInfo(){
    $.ajax({
        url: baseUrl+'/challenges/rippler/',
        method: "POST",
        data: {"action":"getProjectStats", "campaign":campaign},
        dataType: "JSON",
        success: function(response){
            //console.log(response);
            $('#amt_funded > .big_num').html("  " + Math.floor(response['amt_funded']) + " AED");
            $('#num_funders').html(" " + response['num_funders'] + " Funders");
            $('#num_challenges').html(response['num_challenges'] + " Challeges");
            prevDonations();
        },
        error: function(xhr, status, error){
            console.log("Error in getProjectInfo method: " + xhr.responseText);
        }
    })  
}

/* Returns the last n resolved donations */ 
function prevDonations(){
    $.ajax({
        url: baseUrl+'/challenges/rippler/',
        method: "POST",
        data: {"action":"prevDonations", "n": 1000, "campaign":campaign},
        dataType: "json",
        success:function(response){
            donations = response['donations'];
            prevChallenges();
            if(has_donation){
                afterSubmit(donation_condition, donation_amt);
            }

        },
        error: function(xhr, status, error){
            console.log("Error in prevDonations: " + xhr.responseText);
        }
    })
}

/* Returns unresolved donation challenges */
function prevChallenges(){
    var list = [];
    $.ajax({
        url: baseUrl+'/challenges/rippler/',
        method: "POST",
        data: {"action": "prevChallenges", "campaign":campaign},
        dataType: "json",
        success:function(response){
            // console.log(response['challenges']);
            challenges = response['challenges'];
            
            // console.log(user);
            if(user){
                checkForChallenges();
                getChallengesForAmount(user, 20);
            }
            else{
                // console.log("not logged in");
                getPublicChallenges();

            }
        },
        error: function(xhr, status, error){
            console.log("Error in Challenges: " + xhr.responseText);
        }
    })
}

/* Processes a donation_condition in the "explore" or "submit" states */ 
function processDonation(donationCondition, state, challengees){
    console.log(donationCondition);
    $.ajax({
        url: baseUrl+'/challenges/rippler/',
        method: "POST",
        data: {"action":"processDonation", "user": user, 
        "donation": donationCondition, "state": state, 
        "challengees": challengees, "campaign":campaign},
        dataType: "JSON",
        success: function(response){
            // console.log(state);
            // console.log(response);
            var total_impact = response['impact'];
            var donation_amt = donationCondition.split(" ");

            //Update values
            $('#donation_amt').val(donation_amt[0]);
            $('#your_donation').html(parseInt(donation_amt[0]) + " AED");


            curr_donation = {"name": user, "donation": donation_amt[0], "condition": donationCondition, "challengees": challengees};

            // if(donations.length > 0)
            //     regularVisualization(donations, curr_donation, response['change']);

            getChallengesForAmount(user, parseInt(donation_amt[0]));
            if(state == "submit"){
                getProjectInfo();
                //survey(donation_condition, parseInt(donation_amt[0]));
                donation_condition = donationCondition;
                donation_amt = parseInt(donation_amt[0]);
                // afterSubmit(donationCondition, parseInt(donation_amt[0]));
            }
        },
        error: function(xhr, status, error){
            console.log( "Error in processDonation: " +  xhr.responseText);
            //console.log( "Status: " + status );
        }
    }); 
}

/* Returns list of challenges for the user */
function checkForChallenges(){
    $.ajax({
        url: baseUrl+'/challenges/rippler/',
        method: "POST",
        data: {"action":"checkForChallenges", "user": user},
        dataType: "json",
        success: function(response){
            // console.log("You've been challenged " + response['challenge'].length +  " times.");

            notifications = response['challenge'];

            if(response['challenge'].length == 0){
                $('#notifications').hide();
            }

            if(!has_donation)
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
            console.log( "Error in checkForChallenges: " + xhr.responseText);
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

                    if(friend != user){
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
        var donation_amt = $('#friendly').find('#t1_donation_amount').val();
        var count = $('#friendly').find(".friendcount").length;
        var friend = $('#friendly').find('#friends').val();
        

        // console.log("why no work?");
        var friend_amt = $('#friendly').find('#friend_amount').val();
        if(friend_amt.toString().indexOf('.') > -1){
            friend_amt = Math.floor(friend_amt);
        }

        if(friend != "" && sanitizeString(friend)){
            friend_string = friend + " HAS > " + friend_amt;
            friends += friend;
            if(friend == user){
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

                    if(friend == user){
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
        var donation_amt = $('#micro').find('#t3_donation_amount').val();
        var num_people = $('#micro').find('#num_people').val();
        if(num_people.toString().indexOf('.') > -1){
            num_people = Math.floor(num_people);
        }
        var micro_amt = $('#micro').find('#micro_amount').val();
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
/*
function survey(donation_condition, donation){

    $('#donation').remove();
    $('#challenge').remove();
    $('#OR').remove();
    $('#notifications').remove();
    var campaign_qs = "<fieldset>" + 
            "<div>Q: <b>(Required)</b> How much do you care about the health of cats/kittens on campus? <br>" + 
            "<b>Very little</b>     <input type='radio' name='campaign_effect' id='campaign_effect' value='1' >   1   " +
            "<input type='radio' name='campaign_effect' id='campaign_effect' value='2' >   2   " +
            "<input type='radio' name='campaign_effect' id='campaign_effect' value='3' >   3   " +
            "<input type='radio' name='campaign_effect' id='campaign_effect' value='4' >   4   " +
            "<input type='radio' name='campaign_effect' id='campaign_effect' value='5' >   5      <b>A lot</b>" +
        "</div></fieldset>"; 


    var control_qs = "<fieldset><div>" + 
            "Q: <b>(Required)</b> How much would knowing who else donated to the cause affect your donation?<br>" + 
            "<b>Very little</b>     <input type='radio' name='knowing_effect' id='knowing_effect' value='1' >   1   " + 
            "<input type='radio' name='knowing_effect' id='knowing_effect' value='2' >   2   " + 
            "<input type='radio' name='knowing_effect' id='knowing_effect' value='3' >   3   " +  
            "<input type='radio' name='knowing_effect' id='knowing_effect' value='4' >   4   " + 
            "<input type='radio' name='knowing_effect' id='knowing_effect' value='5' >   5    <b>A lot</b></div>   " + 
            "<div> Q: <b>(Required)</b> If you had the ability to challenge other people to donate money to the cause, how likely are you to use it?<br>" + 
            "<b>Not likely</b>      <input type='radio' name='challenge_effect' id='challenge_effect' value='1' >   1   " + 
            "<input type='radio' name='challenge_effect' id='challenge_effect' value='2' >   2   " + 
            "<input type='radio' name='challenge_effect' id='challenge_effect' value='3' >   3   " +  
            "<input type='radio' name='challenge_effect' id='challenge_effect' value='4' >   4   " + 
            "<input type='radio' name='challenge_effect' id='challenge_effect' value='5' >   5     <b>Very likely</b></div>   " + 
            "<div>Q: In what ways would you challenge others?<br><textarea id='challenge_preferences_control' name='challenge_preferences_control' width='100'></textarea></div></fieldset>";


    var conditional_qs_test = "<fieldset><div>" + 
            "Q: <b>(Required)</b> How did you like donation challenges? <br>" + 
            "<b>Not at all</b>      <input type='radio' name='conditional_effect' id='conditional_effect' value='1' >   1   " + 
            "<input type='radio' name='conditional_effect' id='conditional_effect' value='2' >   2   " + 
            "<input type='radio' name='conditional_effect' id='conditional_effect' value='3' >   3   " +  
            "<input type='radio' name='conditional_effect' id='conditional_effect' value='4' >   4   " + 
            "<input type='radio' name='conditional_effect' id='conditional_effect' value='5' >   5      <b>A lot</b></div>   " + 
            "<div>Q: <b>(Required)</b> How likely are you to donate if a friend challenges you?<br>" +
            "<b>Not likely</b>       <input type='radio' name='challenge_effect' id='challenge_effect' value='1' >   1   " + 
            "<input type='radio' name='challenge_effect' id='challenge_effect' value='2' >   2   " + 
            "<input type='radio' name='challenge_effect' id='challenge_effect' value='3' >   3   " +  
            "<input type='radio' name='challenge_effect' id='challenge_effect' value='4' >   4   " + 
            "<input type='radio' name='challenge_effect' id='challenge_effect' value='5' >   5           <b>Very likely</b></div>   " + 
            "<div>Q: How did the challenges influence your donation amount?<br><textarea id='conditional_thoughts' name='conditional_thoughts' width='100'></textarea></div>" + 
            "<div>Q: What other kinds of conditions on donations would you like to be able to make?<br><textarea id='challenge_preferences' name='challenge_preferences' width='100'></textarea></div></fieldset>";

    var interface_qs = "<fieldset><div>" + 
            "Q: <b>(Required)</b> How easy was it to use the website to make a donation? <br>" +
            "<b>Not easy at all </b>     <input type='radio' name='interface_effect' id='interface_effect' value='1' >   1   " +
            "<input type='radio' name='interface_effect' id='interface_effect' value='2' >   2   " + 
            "<input type='radio' name='interface_effect' id='interface_effect' value='3' >   3   " + 
            "<input type='radio' name='interface_effect' id='interface_effect' value='4' >   4   " +
            "<input type='radio' name='interface_effect' id='interface_effect' value='5' >   5   <b>Very easy</b>" +
        "</div><div>Q: Please give us any other comments to improve our system.<br><textarea id='interface_thoughts' width='100' name='interface_thoughts'></textarea></div></fieldset>";


    if(system == "control"){
        $('#thankyou > .container').append("<h3>Thank you for donating, " + user+ "!</h3><form id='survey'><div>Please help us by filling out the survey below. You will then be directed to the confirmation screen.<br><br></div> " + campaign_qs + " " + control_qs + " " + interface_qs + " <button id='survey_submit' class='button-primary'>Next</button></form>");
    }else{
        $('#thankyou > .container').append("<h3>Thank you for donating, " + user+ "!</h3><form id='survey'><div>Please help us by filling out the survey below. You will then be directed to the confirmation screen.<br><br></div> " + campaign_qs + " " + conditional_qs_test +" " + interface_qs + "<button id='survey_submit' class='button-primary'>Next</button></form>");
    }

    $('#survey_submit').click(function(e){
        e.preventDefault();


        var campaign_effect = -1;
        var conditional_effect = -1;
        var challenge_effect = -1;
        var knowing_effect = -1;
        var challenge_preferences_control = "";
        var conditional_thoughts = "";
        var challenge_preferences = "";
        var interface_effect = -1;
        var interface_thoughts = "";

        campaign_effect = $('input:radio[name=campaign_effect]:checked').val();
        interface_effect = $('input:radio[name=interface_effect]:checked').val();
        interface_thoughts = $('#interface_thoughts').val();

        //validate survey responses
        if(system == "control"){
            knowing_effect = $('input:radio[name=knowing_effect]:checked').val();
            challenge_preferences_control = $('#challenge_preferences_control').val();
            challenge_effect = $('input:radio[name=challenge_effect]:checked').val();
            if(!campaign_effect || !interface_effect || !knowing_effect || !challenge_effect){
                $('#survey').prepend("<div id='message' class='dark' style='padding: 2%; color: white;'>Please select responses to required questions.</div>");
                return false;
            }
        }

        else if(system == "test"){
             conditional_effect = $('input:radio[name=conditional_effect]:checked').val();
             challenge_effect = $('input:radio[name=challenge_effect]:checked').val();
             conditional_thoughts = $('#conditional_thoughts').val();
             challenge_preferences = $('#challenge_preferences').val();

            if( !campaign_effect || !interface_effect || !conditional_effect){
                $('#survey').prepend("<div id='message' class='dark' style='padding: 2%; color: white;'>Please select responses to required questions.</div>");
                return false;
            }
        }



        var sendData = {"campaign_effect": campaign_effect, 
                        "conditional_effect": conditional_effect,
                        "challenge_effect": challenge_effect,
                        "knowing_effect":knowing_effect,
                        "challenge_preferences_control": challenge_preferences_control,
                        "challenge_preferences": challenge_preferences,
                        "conditional_thoughts" : conditional_thoughts,  
                        "interface_effect": interface_effect,   
                        "interface_thoughts": interface_thoughts}
        console.log(sendData);

        $.ajax({
            url: baseUrl+'/challenges/rippler',
            method: "POST",
            data: {"user": user, "data": sendData, "system": system},
            dataType: "JSON",
            success:function(response){
        
                 afterSubmit(donation_condition, donation);
            },
            error: function(xhr, status, error){
                console.log("Error: " + error);
            }
        })


       
    })
}*/

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



