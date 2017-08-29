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
    //when click on show comments
    $('.get-comments-btn').click(function(){
        if( $(this).parent().parent().nextAll('.post-comments').css('display') == 'none'){
            //get form options 
            var form_id = '#' + $(this).parent().attr('id');
            var type = $(form_id).attr('method');
            var url = $(form_id).attr('action');
            //call get_comments()
            get_comments(form_id,type,url);
        }
        else if( $(this).parent().parent().nextAll('.post-comments').css('display') == 'block'){
            $(this).html('<i class="fa fa-comments" aria-hidden="true"></i><span> إظهار التعليقات</span>');
            $(this).parent().parent().nextAll('.post-comments').slideUp(function(){
                $(this).html('');
            });
        }
    });
    function get_comments(form_id,type,url){
        var form_id = form_id;
        var type = type;
        var url = url;
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
                    //clear old comments
                    $(form_id).parent().nextAll('.post-comments').html('');
                    //show no-comments note
                    $(form_id).parent().parent().children('.post-body').children('.post-content').children('.no-comments-note').slideDown(200);
                }
                else{
                    //hidden no-comments-note
                    $(form_id).parent().parent().children('.post-body').children('.post-content').children('.no-comments-note').css('display','none');
                    //clear old comments
                    $(form_id).parent().nextAll('.post-comments').html('');
                    //add each comment to comments section 
                    for(var i= result.length ; i > 0 ; i--){
                        var comment = '<div class="comment"><form action="/api/comments/delete" method="post" id="delete-comment-form' + result[i-1].id + '"><input type="hidden" name="comment_id" value="' + result[i-1].id + '" class="comment_id_holder"><p class="publisher-name"> ' + result[i-1].user + '</p><p class="comment-content"> ' + result[i-1].content + '</p><span class="comment-time">' + result[i-1].last_modified + '</span><i class="fa fa-trash comment-delet" aria-hidden="true"></i></form></div>';
                        $(form_id).parent().nextAll('.post-comments').append(comment);
                    }
                    //change button text
                    $(form_id).children('.get-comments-btn').html('<i class="fa fa-comments" aria-hidden="true"></i><span> إخفاء التعليقات</span>');
                    //show comments section 
                    $(form_id).parent().nextAll('.post-comments').slideDown();
                    $(form_id).parent().nextAll('.post-comments').css('overflow-y','auto');
                    
                    
                    //- delete comment 
                    $('.comment-delet').click(function(){
                        var comment_form_id = '#' + $(this).parent().attr('id');
                        var comment_form_type = $(this).parent().attr('method');
                        var comment_form_url = $(this).parent().attr('action');
                        delete_comment(comment_form_id,comment_form_type,comment_form_url);
                    });
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
    //-------------------------------------------- add comment 
    //get form options and call add_comment()
    $('.add-comment-btn').click(function(){
        //get options for ajax
        var form_id = '#' + $(this).parent().attr('id');
        var type = $(form_id).attr('method');
        var url = $(form_id).attr('action');
        //call add_comment function
        add_comment(form_id,type,url);
    });
    //prevent enter from submiting add-comment-form && call add_comment()
    $('.comment-content').keydown(function(event){
        if(event.keyCode == 13){
            event.preventDefault();
            //click on add-comment-btn
            $(this).next('.add-comment-btn').trigger('click');
        }
    });
    function add_comment(form_id,type,url){
        var form_id = form_id;
        var type = type;
        var url = url;
        // send ajax
        $.ajax({
            type: type,
            url: url,
            data: $(form_id).serialize(),
            beforeSend: function(){
                console.log('start add comment');
            },
            success: function(responseText){
                var res = JSON.parse(responseText);
                if(res.result == 'failure'){
                    alert("you can't comment on this post");
                }
                else if( res.result == 'success'){
                    //get options for get_comments()
                    var get_comments_form_id = '#' + $(form_id).parent().parent().children('.show-hide-comments').children('form').attr('id');
                    var get_comments_form_type = $(get_comments_form_id).attr('method');
                    var get_comments_form_url = $(get_comments_form_id).attr('action');
                    //call get_comments()
                    get_comments(get_comments_form_id,get_comments_form_type,get_comments_form_url);
                }
                //clear comment content input
                $(form_id).children('.comment-content').val('');
                
            },
            error: function(error){
                alert("حدث خطأ اثناء الارسال ، برجاء المحاوله مره اخرى");
            }
        });
    }//end of add_comment()
    
    //---------------------------------------------- delete comment 
    // using jQuery to get csrftoken
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    
    // call inside get_comments() to can access comments
    function delete_comment(form_id,type,url){
        var form_id = form_id;
        var type = type;
        var url = url;
        console.log(form_id);
        console.log(type);
        console.log(url);
        // send ajax
        $.ajax({
            type: type,
            url: url,
            data: $(form_id).serialize(),
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            success: function(responseText){
                console.log(responseText);
                var res = JSON.parse(responseText);
                console.log(res);
                if(res.result == 'failure'){
                    
                }
                else if( res.result == 'success'){
                    //get options for get_comments()
                    var get_comments_form_id = '#' + $(form_id).parent().parent().parent().children('.show-hide-comments').children('form').attr('id');
                    var get_comments_form_type = $(get_comments_form_id).attr('method');
                    var get_comments_form_url = $(get_comments_form_id).attr('action');
                    //call get_comments()
                    get_comments(get_comments_form_id,get_comments_form_type,get_comments_form_url);
                }
            },
            error: function(error){
                alert("حدث خطأ اثناء الارسال ، برجاء المحاوله مره اخرى");
            }
        });
    }
    
    
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
