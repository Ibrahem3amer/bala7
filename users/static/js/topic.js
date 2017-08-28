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
    
    
    //------------------------------- get post comments 
    $('.get-comments-btn').click(function(){
        if( $(this).parent().parent().nextAll('.post-comments').css('display') == 'none'){
            
            //send request
            var form_id = '#' + $(this).parent().attr('id');
            var type = $(form_id).attr('method');
            var url = $(form_id).attr('action');
            $.ajax({
                type: type,
                url: url,
                data: $(form_id).serialize(),
                beforeSend: function(){
                    //show loading
                    $(form_id).children('.loading').css('display','inline-block');
                },
                success: function(result){
                    //hide loading
                    $(form_id).children('.loading').css('display','none');
                    //hidden error note
                    $(form_id).parent().parent().children('.post-body').children('.post-content').children('.error-note').css('display','none');
                    
                    if( result.length == 0){
                        $(form_id).parent().parent().children('.post-body').children('.post-content').children('.no-comments-note').css('display','none');
                        //show no-comments note
                        $(form_id).parent().parent().children('.post-body').children('.post-content').children('.no-comments-note').slideDown(200);
                    }
                    else{
                        //hidden no-comments-note
                        $(form_id).parent().parent().children('.post-body').children('.post-content').children('.no-comments-note').css('display','none');
                        //add each comment to comments section 
                        for(var i=0; i < result.length; i++){
                            var comment = '<div class="comment"><p class="publisher-name"> ' + result[i].user + '</p><p class="comment-content"> ' + result[i].content + '</p><span class="comment-time">' + result[i].last_modified + '</span></div>';
                            $(form_id).parent().nextAll('.post-comments').append(comment);
                        }
                        //change button text
                        $(form_id).children('.get-comments-btn').html('<i class="fa fa-comments" aria-hidden="true"></i><span> إخفاء التعليقات</span>');
                        //show comments section 
                        $(form_id).parent().nextAll('.post-comments').slideDown();
                    }

                },
                error: function(){
                    //hide loading
                    $(form_id).children('.loading').css('display','none');
                    //hide no-comments-note
                    $(form_id).parent().parent().children('.post-body').children('.post-content').children('.no-comments-note').css('display','none');
                    //show hidden note
                    $(form_id).parent().parent().children('.post-body').children('.post-content').children('.error-note').css('display','none');
                    //show error note
                    $(form_id).parent().parent().children('.post-body').children('.post-content').children('.error-note').slideDown(200);
                }
            });//end ajax  
        }
        else if( $(this).parent().parent().nextAll('.post-comments').css('display') == 'block'){
            $(this).html('<i class="fa fa-comments" aria-hidden="true"></i><span> إظهار التعليقات</span>');
            $(this).parent().parent().nextAll('.post-comments').slideUp(function(){
                $(this).html('');
            });
        }
        
        
    });
    
    
    
    //------------------------------- show add new week box
    $('#add-week-btn').click(function(){
        $('#new-week-box').slideToggle();
    });
    //close new week box
    $('.week-head i').click(function(){
        $('#new-week-box').slideUp();
    });
    
    //------------------------------------ edit week
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
