$(document).ready(function(){
    //send ajax to get universites
    $.ajax({url: "/api/universities/", success: function(result){
        var universities = '<option value="" disabled selected>اختر الجامعة</option>';
        for(var i = 0 ; i < result.length ; i++){
            universities += '<option class="university_name" value="'+ result[i].id +'" id="'+ result[i].id +'">'+ result[i].name +'</option>'
        }
        $("#id_select_university").html(universities);
    }});//end ajax
    
    
    //when choose university name then request faculties data and display it
    $("#id_select_university").change(function(){
        //clear other fields
        $("#id_select_faculty").html('<option value="" disabled selected>اختر الكليه</option>');
        $("#id_select_department").html('<option value="" disabled selected>اختر القسم</option>');
        //get the id of selected option
        var universityId = $(this).children(":selected").attr("id");
        //send ajax
        $.ajax({url: "/api/faculties/university/"+ universityId +"", success: function(result){
            var faculties = '<option value="" disabled selected>اختر الكليه</option>';
            for(var i = 0 ; i < result.length ; i++){
                faculties += '<option class="faculty_name" value="'+ result[i].id +'" id="'+ result[i].id +'">'+ result[i].name +'</option>'
            }
            $("#id_select_faculty").html(faculties);
        }});//end ajax
    });
    
    //when choose faculties then request departments data and display it
    $("#id_select_faculty").change(function(){
        //clear other fields
        $("#id_select_department").html('<option value="" disabled selected>اختر القسم</option>');
        //get the id of selected option
        var facultId = $(this).children(":selected").attr("id");
        //send ajax
        $.ajax({url: "/api/departments/faculty/"+ facultId +"", success: function(result){
            var departments = '<option value="" disabled selected>اختر القسم</option>';
            for(var i = 0 ; i < result.length ; i++){
                departments += '<option class="department_name" value="'+ result[i].id +'" id="'+ result[i].id +'">'+ result[i].name +'</option>'
            }
            $("#id_select_department").html(departments);
        }});//end ajax
    });

    
    
    
    
    
});