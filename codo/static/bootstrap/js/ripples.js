var nodes = [];
var links = [];
var ripples = [];

// var user_list = [];
var donations = [];
var challenges = [];

var curr_donation;
var notifications = [];
var has_donation = window.djangoData["has_donation"]

$(document).ready(function(){

   /* $('.form').hide(); 
    // $('#more').hide();
    $('#current_friends').hide();
    // $('#notifications').hide();

    //get user info and project info
    $('#user_name').html(window.user);*/

    var dfd = $.Deferred();
    dfd.done(getProjectInfo())
    .done(function(){
        if(has_donation){
            console.log(window.donations);
            // afterSubmit(donation_condition, donation_amt, impact)
            
        }
        else{
           
            processDonation("20", "explore");
            checkForChallenges();

        }
    });  

    dfd.resolve();


    /***** USER INTERACTIONS *****/

    //Display the appropriate challenge form
    $('.chal_form').on('click', function(){
        var curr_form = $(this).find($('.form')).attr("id");
        $('.chal_form').siblings().children('.form').hide();
        $('.chal_form').siblings().find('img.arrow').show();
        // $('.chal_form').siblings().find('.msg').hide();
  
        $('#' + curr_form).parent().find('img.arrow').hide();
        // $('#' + curr_form).parent().find('.msg').show();
        // $('#' + curr_form).parent().find('.msg').removeClass('msg');
        $('#' + curr_form).show();
    })

    //Friends Challenge - Add button interaction
    $('#addfriend').on('click', function(){
        //Count # of friends added so far
        var count = $(this).parent().find(".friendcount").length;
        

        //add another friend
        var formaddendum = '<div class="newfriend"><br> AND if<br><input type="text" id="friends' + count + '" class="friendcount" placeholder="Enter friend\'s netID"></input> also donates <br>' + 
        '<input type="number" id="friend_amount'+count+'" class="input_amt" min="10" max="1000" value="20"></input> AED (optional)<br>' +
        '<span id="removefriend-"' + count + ' class="link remove"> [-] Remove friend</span></div> ';

        // console.log($(this).prev());
        $(formaddendum).insertAfter($(this).prev());
        if(count == 4){
            $('#addfriend').remove();
            return false;
        }
        

        //Remove friend
        $('.remove').on('click', function(){
            $(this).parent().remove();
        })
    })

   
   

    //Function to get donation amounts that users are exploring with
    $('.amount').on('input',function(){
        var donation_amt = $(this).val()
        if(donation_amt <= 0){
            $(this).val(5);
            $('#curr_donation').html(5);
        }else if(donation_amt.toString().indexOf('.') > -1){
            $(this).val(Math.floor(donation_amt));
        }
        else{
            $('#curr_donation').html(donation_amt);
            processDonation(donation_amt, "explore", "");
            getChallengesForAmount(user, donation_amt);
        }
    });

    $('.input_amt').on('input',function(){
        var donation_amt = $(this).val()
        if(donation_amt <= 0){
            $(this).val(5);
            // $('#curr_donation').html(5);
        }
    });

    $('.friendcount').on('input', function(){
        var str = $(this).val();
        if(/^[a-zA-Z0-9]+$/.test(str) == false){
            
            //display error message
            $('#current_friends').empty();
            $('#current_friends').html("Error: Invalid characters in netID. Only alphabets and numeric digits allowed.");
            $('#current_friends').show();
            $(this).val("");
        }else{
             $('#current_friends').hide();
        }
       
    })


    //Function to get donation conditions users are submitting
    $('.challenge_button').click(function(){
        // console.log($(this));
        var id = $(this).attr("id");
        getDonationCondition(id, "submit");
    })

    $('#donate').click(function(){
        processDonation($('#donation_amount').val(), "submit", "");
    })

})

