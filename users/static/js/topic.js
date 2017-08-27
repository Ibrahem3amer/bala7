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
    
    
    
    //--------------------------- open contribute-form
    $("#contribute-btn").click(function(){
        $("#request-form").fadeOut(function(){
            $("#contribute-form").toggle();
        });
    });
    
    //--------------------------- open request-form
    $("#request-btn").click(function(){
        $("#contribute-form").fadeOut(function(){
            $("#request-form").toggle();
            
        });
    });
    
    //-------------------------------------- start submit contribute-form
    $('#contribution_form').ajaxForm({
        success: function(responseText) { 
            var res = JSON.parse(responseText);
            if( res.result == 'failure'){
                if(res.errors.name){
                    $('#id_name').parent().children('.formLineError').remove();
                    var lineError = '<div class="alert alert-warning formLineError" role="alert"> ' + res.errors.name + '</div>';
                    $('#id_name').parent().prepend(lineError);
                }else{ $('#id_name').parent().children('.formLineError').remove(); }

                if(res.errors.content){
                    $('#id_content').parent().children('.formLineError').remove();
                    var lineError = '<div class="alert alert-warning formLineError" role="alert">' + res.errors.content + '</div>';
                    $('#id_content').parent().prepend(lineError);
                }else{ $('#id_content').parent().children('.formLineError').remove(); }

                if(res.errors.link){
                    $('#id_link').parent().children('.formLineError').remove();
                    var lineError = '<div class="alert alert-warning formLineError" role="alert">' + res.errors.link + '</div>';
                    $('#id_link').parent().prepend(lineError);
                }else{ $('#id_link').parent().children('.formLineError').remove(); }

                if(res.errors.__all__){//week number
                    $('#id_week_number').parent().children('.formLineError').remove();
                    var lineError = '<div class="alert alert-warning formLineError" role="alert">' + res.errors.__all__ + '</div>';
                    $('#id_week_number').parent().prepend(lineError);
                }else{ $('#id_week_number').parent().children('.formLineError').remove(); }     

            }else if ( res.result == 'success'){
                $('.share-box-body .contribution_form-body').fadeOut(function(){
                    $('.share-box-body .success-div').fadeIn();
                });
            }
        },//end of success
        error: function(){
            $('.share-box-body .contribution_form-body').fadeOut(function(){
                $('.share-box-body .errors-div').fadeIn();
            });
        }//end of error
    }); 
    
    //-------------------------------------- start submit order-box
    $('#post_form').ajaxForm({
        success: function(responseText) { 
            var res = JSON.parse(responseText);
            console.log(res.errors);
            if( res.result == 'failure'){
                if(res.errors.title){
                    $('#id_title').parent().children('.formLineError').remove();
                    var lineError = '<div class="alert alert-warning formLineError" role="alert"> ' + res.errors.title + '</div>';
                    $('#id_title').parent().prepend(lineError);
                }else{ $('#id_title').parent().children('.formLineError').remove(); }    
            }else if ( res.result == 'success'){
                $('.order-box-body .post_form-body').fadeOut(function(){
                    $('.order-box-body .success-div').fadeIn();
                });
            }
        },//end of success
        error: function(){
            $('.order-box-body .post_form-body').fadeOut(function(){
                $('.order-box-body .errors-div').fadeIn();
            });
        }//end of error
    });
    
    //close share-box
    $('.share-box .box-close-btn').click(function(){
        $('.share-box .success-div').fadeOut(1);
        $('.share-box .errors-div').fadeOut(1);
        $(this).parent().parent().parent().fadeOut(function(){
            $('.share-box .contribution_form-body .formLineError').remove();
            $('#contribution_form').trigger('reset');
            $('.share-box .contribution_form-body').fadeIn(1);
        });
        
    });
    //close order-box
    $('.order-box .box-close-btn').click(function(){
        $('.order-box .success-div').fadeOut(1);
        $('.order-box .errors-div').fadeOut(1);
        $(this).parent().parent().parent().fadeOut(function(){
            $('.order-box .post_form-body .formLineError').remove();
            $('#post_form').trigger('reset');
            $('.order-box .post_form-body').fadeIn(1);
        });
        
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
    });
    
    //show add new week box
    $('#add-week-btn').click(function(){
        $('#new-week-box').slideToggle();
    });
    //close new week box
    $('.week-head i').click(function(){
        $('#new-week-box').slideUp();
    });
    
    // edit week
    $('.edit-week-icon').click(function(event){
        var weekDisplay = $(this).parent().next().css('display');
        if( weekDisplay == 'none'){
            $(this).removeClass('fa-cog').addClass('fa-times');
            $(this).parent().next().slideDown();
            $(this).parent().next().next().slideUp();
        }else{
            $(this).removeClass('fa-times').addClass('fa-cog');
            $(this).parent().next().slideUp();
            $(this).parent().next().next().slideDown();
        }
    });
    
    
});
