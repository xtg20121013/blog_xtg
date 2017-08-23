function update_disable(url) {
    var _xsrf = getCookie("_xsrf");
    $.post(url, {_xsrf:_xsrf}, function (data) {
        location.reload();
    });
}

function delete_comment(url) {
    var _xsrf = getCookie("_xsrf");
    $.post(url, {_xsrf:_xsrf}, function (data) {
        location.reload();
    });
}

function delCommentCfm(url) {
    $('#delCommentCfmClick').click(function(){
        delete_comment(url);
    });
    $('#delCommentCfmModel').modal();
}

function go_to_reply(comment_type, reply_to_id, reply_to_floor) {
    $('#reply-dialog-box').remove();
    $('#submit-comment-form').prepend('<div class="alert alert-info alert-dismissable" id="reply-dialog-box">' +
            '<input type="hidden" name="comment_type", value="'+comment_type+'">'+
            '<input type="hidden" name="reply_to_id", value="'+reply_to_id+'">'+
            '<input type="hidden" name="reply_to_floor", value="'+reply_to_floor+'">'+
            '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
            '回复给<strong><i>' + reply_to_floor +'</i></strong> </div>');
    $('html, body').animate({scrollTop:$('#submit-comment').offset().top});
}

//Reset the follow value when refresh page
window.onload = function(){
    var content = $('.article-content').text();
    $('.article-content').html(marked(content));
    $('.article-loading').hide();
    $('.article-content').show();
    codeHighLight();
    var scrollName = location.hash;
    if(scrollName) {
        $("body,html").animate({scrollTop: $(scrollName).offset().top}, "fast");
    }
}



