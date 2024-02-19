$(document).ready(function(){


    // On load set the quick access icon
    if(localStorage.q_item_0 != ''){
        $('#q_item_0 i').removeClass(localStorage.q_item_0_c);
        $('#q_item_0 i').addClass(localStorage.q_item_0);

        if ($('#q_button_0 i').attr('class') == 'empty'){
            $('#q_button_0 i').removeClass('empty');
            $('#q_button_0 i').addClass(localStorage.q_item_0);
        } else{
            $('#q_button_0 i').removeClass(localStorage.q_item_0_c);
            $('#q_button_0 i').addClass(localStorage.q_item_0);
        }
    }
    if(localStorage.q_item_1 != ''){
        $('#q_item_1 i').removeClass(localStorage.q_item_1_c);
        $('#q_item_1 i').addClass(localStorage.q_item_1);

        if ($('#q_button_1 i').attr('class') == 'empty'){
            $('#q_button_1 i').removeClass('empty');
            $('#q_button_1 i').addClass(localStorage.q_item_1);
        } else{
            $('#q_button_1 i').removeClass(localStorage.q_item_1_c);
            $('#q_button_1 i').addClass(localStorage.q_item_1);
        }
    }
    if(localStorage.q_item_2 != ''){
        $('#q_item_2 i').removeClass(localStorage.q_item_2_c);
        $('#q_item_2 i').addClass(localStorage.q_item_2);

        if ($('#q_button_2 i').attr('class') == 'empty'){
            $('#q_button_2 i').removeClass('empty');
            $('#q_button_2 i').addClass(localStorage.q_item_2);
        } else{
            $('#q_button_2 i').removeClass(localStorage.q_item_2_c);
            $('#q_button_2 i').addClass(localStorage.q_item_2);
        }
    }
    if(localStorage.q_item_3 != ''){
        $('#q_item_3 i').removeClass(localStorage.q_item_3_c);
        $('#q_item_3 i').addClass(localStorage.q_item_3);

        if ($('#q_button_3 i').attr('class') == 'empty'){
            $('#q_button_3 i').removeClass('empty');
            $('#q_button_3 i').addClass(localStorage.q_item_3);
        } else{
            $('#q_button_3 i').removeClass(localStorage.q_item_3_c);
            $('#q_button_3 i').addClass(localStorage.q_item_3);
        }
    }
    if(localStorage.q_item_4 != ''){
        $('#q_item_4  i').removeClass(localStorage.q_item_4_c);
        $('#q_item_4  i').addClass(localStorage.q_item_4);

        if ($('#q_button_4  i').attr('class') == 'empty'){
            $('#q_button_4  i').removeClass('empty');
            $('#q_button_4  i').addClass(localStorage.q_item_4);
        } else{
            $('#q_button_4  i').removeClass(localStorage.q_item_4_c);
            $('#q_button_4 i').addClass(localStorage.q_item_4);
        }
    }

    // On load set url
    if(localStorage.href_ls_0 != ''){ $('div.q_item_setting input#url0').val(localStorage.href_ls_0); }
    if(localStorage.href_ls_1 != ''){ $('div.q_item_setting input#url1').val(localStorage.href_ls_1); }
    if(localStorage.href_ls_2 != ''){ $('div.q_item_setting input#url2').val(localStorage.href_ls_2); }
    if(localStorage.href_ls_3 != ''){ $('div.q_item_setting input#url3').val(localStorage.href_ls_3); }
    if(localStorage.href_ls_4 != ''){ $('div.q_item_setting input#url4').val(localStorage.href_ls_4); }

    // On load set selection of target type
    if(localStorage.select_target_ls_0 != ''){ $('#selectTargetType0').val(localStorage.select_target_ls_0); }
    if(localStorage.select_target_ls_1 != ''){ $('#selectTargetType1').val(localStorage.select_target_ls_1); }
    if(localStorage.select_target_ls_2 != ''){ $('#selectTargetType2').val(localStorage.select_target_ls_2); }
    if(localStorage.select_target_ls_3 != ''){ $('#selectTargetType3').val(localStorage.select_target_ls_3); }
    if(localStorage.select_target_ls_4 != ''){ $('#selectTargetType4').val(localStorage.select_target_ls_4); }


    // Onclick on close button
    $('div.q_setting_close i').click(function(){

        // Check if setting window is open to toggle setting window class
        if ($('#q_settings').hasClass('q_setting_open')){ $('#q_settings').toggleClass('q_setting_open'); }
    });

    // Onclick on navigation button "main button"
    $("#q_main").click(function(){
        $('#q_main').toggleClass('q_items_open');




        // Check if setting window is open to toggle setting window class
        if ($('#q_settings').hasClass('q_setting_open')){ $('#q_settings').toggleClass('q_setting_open'); }

        if($('div#q_main').hasClass('q_items_open')) {
           $('div.q_item_0').css({'top': '-150px'});
           $('div.q_item_1').css({'top': '-133px','left': '-52px'});
           $('div.q_item_2').css({'top': '-101px','left': '-99px'});
           $('div.q_item_3').css({'top': '-55px','left': '-130px'});
           $('div.q_item_4').css({'left': '-144px'});
           $('div.q_settings').css({'top':'-82px','left': '4px'});

           $('div.q_item i').css({'opacity':1});
           $('div.q_settings i').css({'opacity':1});
        }
        else {
           $('div.q_item_0').css('top', 0);
           $('div.q_item_1').css({'top': 0,'left': 0});
           $('div.q_item_2').css({'top': 0,'left': 0});
           $('div.q_item_3').css({'top': 0,'left': 0});
           $('div.q_item_4').css({'top': 0,'left': 0});
           $('div.q_settings').css({'top':'2px','left': '3px'});

           $('div.q_item i').css({'opacity':0});
           $('div.q_settings i').css({'opacity':0});
        }

    });

    // Onclick on setting button
    $('#q_settings').click(function(){
        $('#q_settings').toggleClass('q_setting_open');
    });

    // Onclick on save button
    $("#q_save").click(function(){

        // Check if setting window is open to toggle setting window class
        if ($('#q_settings').hasClass('q_setting_open')){
            $('#q_settings').toggleClass('q_setting_open');
        }


        // Get Classes from buttons in setting window
        var class_0 = $('#q_button_0 i').attr('class');
        var class_1 = $('#q_button_1 i').attr('class');
        var class_2 = $('#q_button_2 i').attr('class');
        var class_3 = $('#q_button_3 i').attr('class');
        var class_4 = $('#q_button_4 i').attr('class');

        // Remove Classes from buttons in Quick access
        if (class_0 != 'empty'){
            var current_class_0 = $('#q_item_0 i').attr('class');
            localStorage.q_item_0 =  class_0;
            localStorage.q_item_0_c = current_class_0;
        }
        if (class_1 != 'empty'){
            var current_class_1 = $('#q_item_1 i').attr('class');
            localStorage.q_item_1 =  class_1;
            localStorage.q_item_1_c = current_class_1;
        }
        if (class_2 != 'empty'){
            var current_class_2 = $('#q_item_2 i').attr('class');
            localStorage.q_item_2 =  class_2;
            localStorage.q_item_2_c = current_class_2;
        }
        if (class_3 != 'empty'){
            var current_class_3 = $('#q_item_3 i').attr('class');
            localStorage.q_item_3 =  class_3;
            localStorage.q_item_3_c = current_class_3;
        }
        if (class_4 != 'empty'){
            var current_class_4 = $('#q_item_4 i').attr('class');
            localStorage.q_item_4 =  class_4;
            localStorage.q_item_4_c = current_class_4;
        }

        // Get href from a tags in setting window
        var href_0 = $('div.q_item_setting input#url0').val();
        var href_1 = $('div.q_item_setting input#url1').val();
        var href_2 = $('div.q_item_setting input#url2').val();
        var href_3 = $('div.q_item_setting input#url3').val();
        var href_4 = $('div.q_item_setting input#url4').val();

        // Store all href in local storage
        localStorage.href_ls_0 = href_0;
        localStorage.href_ls_1 = href_1;
        localStorage.href_ls_2 = href_2;
        localStorage.href_ls_3 = href_3;
        localStorage.href_ls_4 = href_4;

        // Get selection field of target type
        var select_target_0 = $('#selectTargetType0').val();
        var select_target_1 = $('#selectTargetType1').val();
        var select_target_2 = $('#selectTargetType2').val();
        var select_target_3 = $('#selectTargetType3').val();
        var select_target_4 = $('#selectTargetType4').val();

        // Store all selection field of target type
        localStorage.select_target_ls_0 = select_target_0;
        localStorage.select_target_ls_1 = select_target_1;
        localStorage.select_target_ls_2 = select_target_2;
        localStorage.select_target_ls_3 = select_target_3;
        localStorage.select_target_ls_4 = select_target_4;


  });
  });