$(document).ready(function(){


    function hasClasses(element, cls) {
        return (' ' + element.className + ' ').indexOf(' ' + cls + ' ') > -1;
    }


    var iframe = document.getElementById("iFrame_navigation");
    iframe.onload = function() {
        var saveButton = iframe.contentWindow.document.getElementById("q_save");
        var closeButton = iframe.contentWindow.document.getElementById("q_setting_close");
        var openSettings = iframe.contentWindow.document.getElementById("q_settings");
        var settingsWindow = iframe.contentWindow.document.getElementById("q_setting_container");
        var openNavigation = iframe.contentWindow.document.getElementById("q_main");
        var navigationElement_0 = iframe.contentWindow.document.getElementById("q_item_0");
        var navigationElement_1 = iframe.contentWindow.document.getElementById("q_item_1");
        var navigationElement_2 = iframe.contentWindow.document.getElementById("q_item_2");
        var navigationElement_3 = iframe.contentWindow.document.getElementById("q_item_3");
        var navigationElement_4 = iframe.contentWindow.document.getElementById("q_item_4");

        closeButton.onclick = function(){
            settingsWindow.style.opacity = 0;
                setTimeout(function(){
                    iframe.width = 250;
                    iframe.height = 250;
                },300);
        };
        saveButton.onclick = function(){
            settingsWindow.style.opacity = 0;
                setTimeout(function(){
                    iframe.width = 250;
                    iframe.height = 250;
                },300);

            location.reload();  // Reload the bage

        };
        openSettings.onclick = function(){

            if (hasClasses(openSettings,"q_setting_open")){
                iframe.width = '90%';
                iframe.height = '90%';
                settingsWindow.style.opacity = 1;
            }
            else{
                settingsWindow.style.opacity = 0;
                setTimeout(function(){
                    iframe.width = 250;
                    iframe.height = 250;
                },300);
            }
        };
        openNavigation.onclick = function(){

            if (hasClasses(openNavigation,"q_items_open")){
                iframe.width = 250;
                iframe.height = 250;
            }else{
                settingsWindow.style.opacity = 0;
                setTimeout(function(){
                    iframe.width = 65;
                    iframe.height = 60;
                }, 750);
            }

        };
        navigationElement_0.onclick = function(){
            if(localStorage.href_ls_0 !=''){
                if(localStorage.select_target_ls_0 == 'Open in Current Window'){window.open(localStorage.href_ls_0, '_self');}
                else{
                window.open(localStorage.href_ls_0, '_blank');
                }
            }
        };
        navigationElement_1.onclick = function(){
            if(localStorage.href_ls_1 !=''){
                if(localStorage.select_target_ls_1 == 'Open in Current Window'){window.open(localStorage.href_ls_1, '_self');}
                else{
                window.open(localStorage.href_ls_1, '_blank');
                }
            }
        };
        navigationElement_2.onclick = function(){
            if(localStorage.href_ls_2 !=''){
                if(localStorage.select_target_ls_2 == 'Open in Current Window'){window.open(localStorage.href_ls_2, '_self');}
                else{
                window.open(localStorage.href_ls_2, '_blank');
                }
            }
        };
        navigationElement_3.onclick = function(){
            if(localStorage.href_ls_3 !=''){
                if(localStorage.select_target_ls_3 == 'Open in Current Window'){window.open(localStorage.href_ls_3, '_self');}
                else{
                window.open(localStorage.href_ls_3, '_blank');
                }
            }
        };
        navigationElement_4.onclick = function(){
            if(localStorage.href_ls_4 !=''){
                if(localStorage.select_target_ls_4 == 'Open in Current Window'){window.open(localStorage.href_ls_4, '_self');}
                else{
                window.open(localStorage.href_ls_4, '_blank');
                }
            }
        };


    };


});