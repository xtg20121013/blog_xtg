//JS For FloatButton to goTop, goBottom and refresh
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function getAlertHtml(category, message) {
    var s = '<div class="alert alert-'+category+' alert-dismissable" id="fix-alert">'+
            '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>'+
            message+'</div>';
    return s;
}

function alertXtg(category, message, timeout) {
    s = getAlertHtml(category, message);
    $('body').append(s);
    if(timeout) {
        setTimeout(function () {
            $('#fix-alert').remove();
        }, timeout);
    }
}


$(document).ready(function(){
    //$('#goTop').click(function(){
    //    $(window).scrollTop(0);
    //});
    $('#goTop').click(function(){
        $('html, body').animate({scrollTop: '0px'}, 800);
    });
    $('#refresh').click(function(){
        window.location.reload();
    });
    $('#goBottom').click(function(){
        $('html, body').animate({scrollTop: $('.footer').offset().top}, 800);
    });
});


