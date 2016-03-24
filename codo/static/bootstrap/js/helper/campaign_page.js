$(".paymentPanel").hide();
$(".campaignDescription").show();

$(function(){
$('.clickable').on('click',function(){

    var effect = $(this).data('effect');
        $(this).closest('.panel')[effect]();

    });
    
})


$("#fundprojectBtn").click(function(){
    $(".paymentPanel").toggle();
    $(".campaignDescription").toggle();
});