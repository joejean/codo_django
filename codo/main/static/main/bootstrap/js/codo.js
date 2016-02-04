$(document).ready(function(){
    
    $('.cont').click(function(){

        var nextId = $(this).parents('.tab-pane').next().attr("id")||'step1';
        $('[href=#'+nextId+']').tab('show');

    })

});


