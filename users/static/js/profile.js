$(document).ready(function(){    
    
    //choose-univ-setting
    $('#choose-univ-setting').click(function(){
        $(this).fadeOut(function(){
            $('.univ-info').fadeOut(function(){
                $('.choose-univ').fadeIn();
            });
        });
    });
    
    //choose-materials-srtting
    $('#choose-materials-setting').click(function(){
        $(this).fadeOut(function(){
            $('.materials').fadeOut(function(){
                $('.choose-materials').fadeIn();
            });
        });
    });
    //change checkbox on chick 
    $("input[type='checkbox']").change(function(){
        if($(this).is(":checked")){
            $(this).parent().addClass("active-checkbox"); 
        }else{
            $(this).parent().removeClass("active-checkbox");  
        }
    });
    
});
