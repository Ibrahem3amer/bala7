$(document).ready(function(){
    
    //right div out
    $('#right-arrow').click(function(){
        $('.right-div').animate({right: "-295px"});
        $(this).fadeOut(function(){
            $('#left-arrow').fadeIn();
        }); 
    });
    //left div enter
    $('#left-arrow').click(function(){
        $('.right-div').animate({right: "0px"});
        $('#left-arrow').fadeOut(function(){
            $('#right-arrow').fadeIn();
        });
    });
    
    
    
    
    $("#contribute-form").fadeOut()
    $("#contribute-btn").click(function(){
        $("#request-form").fadeOut(function(){
            $("#contribute-form").toggle();
        });
    });
    
    $("#request-form").fadeOut()
    $("#request-btn").click(function(){
        $("#contribute-form").fadeOut(function(){
            $("#request-form").toggle();
        });
    });
    
    //close btn for share-box and order-box
    $('.box-close-btn').click(function(){
        $(this).parent().fadeOut();
    });
    
    //show and hide comments
    $('.show-hide-comments p').click(function(){
        if( $(this).parent().nextAll('.post-comments').css('display') == 'none'){
            $(this).html('<i class="fa fa-comments" aria-hidden="true"></i><span> إخفاء التعليقات</span>');
            $(this).parent().nextAll('.post-comments').fadeIn();
        }
        else if( $(this).parent().nextAll('.post-comments').css('display') == 'block'){
            $(this).html('<i class="fa fa-comments" aria-hidden="true"></i><span> إظهار التعليقات</span>');
            $(this).parent().nextAll('.post-comments').fadeOut();
        }
    })
});
