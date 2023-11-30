var preloader = $(".preloader");

$(document).ready(function() {

    /* LOADER */
    $(window).on("load", function() {
        $(preloader).fadeOut();
    });
    setTimeout(function() {
        if ($(preloader).css("display") != "none") {
            $(preloader).fadeOut();
        }
    }, 7000);
    
});
