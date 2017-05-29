$(document).ready(function(){    
    
    //choose-univ-setting
    $('#choose-univ-setting').click(function(){
        $(this).fadeOut(function(){
            $('.univ-info').fadeOut(function(){
                $('.choose-univ').fadeIn(function(){
                    $('#universities-selector-div').fadeIn();
                    //send ajax
                    $.ajax({url: "/api/universities/", success: function(result){
                        var universities = '<option value="" disabled selected>اختر الجامعة</option>';
                        for(var i = 0 ; i < result.length ; i++){
                            universities += '<option id="'+ result[i].id +'">'+ result[i].name +'</option>'
                        }
                        $("#universities-selector").html(universities);
                    }});//end ajax
                });
            
            });
        });
    });
    
        //when choose university name then request faculties data and display it
        $("#universities-selector").change(function(){
            //get the id of selected option
            var universityId = $(this).children(":selected").attr("id");
            //set #universities-hidden
            $('#universities-hidden').val(universityId);
            //reset and fadeout submit button , #departments-selector-div and #section-div
            $('.choose-univ .true-submit-btn').fadeOut();
            $('#departments-selector').html('<option value="" disabled selected>اختر القسم</option>');
            $('#departments-selector-div').fadeOut('fast');
            $('#section-div').fadeOut('fast');
            $('#faculties-hidden').val("");
            $('#departments-hidden').val("");
            //display faculties selector
            $('#faculties-selector-div').fadeIn(function(){
                //send ajax
                $.ajax({url: "/api/faculties/university/"+ universityId +"", success: function(result){
                    var faculties = '<option value="" disabled selected>اختر الكليه</option>';
                    for(var i = 0 ; i < result.length ; i++){
                        faculties += '<option id="'+ result[i].id +'">'+ result[i].name +'</option>'
                    }
                    $("#faculties-selector").html(faculties);
                }});//end ajax
            });
        });
        
        //when choose faculties then request departments data and display it
        $("#faculties-selector").change(function(){
            //get the id of selected option
            var facultId = $(this).children(":selected").attr("id");
            //set faculties-hidden
            $('#faculties-hidden').val(facultId);
            //fadeout submit button and #section-div
            $('.choose-univ .true-submit-btn').fadeOut();
            $('#section-div').fadeOut('fast');
            //reset #departments-hidden
            $('#departments-hidden').val("");
            //display faculties selector
            $('#departments-selector-div').fadeIn(function(){
                //send ajax
                $.ajax({url: "/api/departments/faculty/"+ facultId +"", success: function(result){
                    var departments = '<option value="" disabled selected>اختر القسم</option>';
                    for(var i = 0 ; i < result.length ; i++){
                        departments += '<option id="'+ result[i].id +'">'+ result[i].name +'</option>'
                    }
                    $("#departments-selector").html(departments);
                }});//end ajax
            });
        });
    
        //when choose department then display section
        $("#departments-selector").change(function(){
            //get the id of selected option
            var departmentId = $(this).children(":selected").attr("id");
            //set universities-hidden
            $('#departments-hidden').val(departmentId);
            
            $('#section-div').fadeIn(); 
        });
    
        //display submit button when fill section 
        $("#section-input").change(function(){
            if($("#section-input").val() == ""){
                $('.choose-univ .true-submit-btn').fadeOut();
            }
            else{
                $('.choose-univ .true-submit-btn').fadeIn();
            }
        });
        $("#section-input").keyup(function(){
            if($("#section-input").val() == ""){
                $('.choose-univ .true-submit-btn').fadeOut();
            }
            else{
                $('.choose-univ .true-submit-btn').fadeIn();
            }
        });
    
    
    
    //------------------------------------------------------------------------------------------------------
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

