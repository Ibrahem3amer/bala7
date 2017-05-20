$(document).ready(function(){    
    
    //choose-univ-setting
    $('#choose-univ-setting').click(function(){
        if($(this).attr('class') == 'fa fa-cog'){
            $('.univ-info').fadeOut(function(){
                $('.choose-univ').fadeIn();
            });
            
            
            $(this).removeClass('fa-cog');
            $(this).addClass('fa-check');
        }
        else if($(this).attr('class') == 'fa fa-check'){
            $('.choose-univ').fadeOut(function(){
                $('.univ-info').fadeIn();
            });
            
            
            $(this).addClass('fa-cog');
            $(this).removeClass('fa-check');
        }
    });
    
    //choose-materials-srtting
    $('#choose-materials-setting').click(function(){
        if($(this).attr('class') == 'fa fa-cog'){
            $('.materials').fadeOut(function(){
                $('.choose-materials').fadeIn();
            });
            
            
            $(this).removeClass('fa-cog');
            $(this).addClass('fa-check');
        }
        else if($(this).attr('class') == 'fa fa-check'){
            $('.choose-materials').fadeOut(function(){
                $('.materials').fadeIn();
            });
            
            
            $(this).addClass('fa-cog');
            $(this).removeClass('fa-check');
        }
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
