//JS For manage-articles when select articles or select comments
$(document).ready(function () {
    $('#select-all').click(function () {
        if ($(this).prop('checked')) {
            $('.op_check').prop('checked', true);
        } else {
            $('.op_check').prop('checked', false);
        }
    });
});

//JS For submit article id to delete article
function delCfm(delLink) {
    $('#cfmClick').click(function () {
        var _xsrf = getCookie("_xsrf");
        $.post(delLink, {_xsrf:_xsrf}, function () {
            location.reload();
        });
    });
    $('#delCfmModel').modal();
}

//JS For select articles to delete
$(document).ready(function () {
    $('#delArtsCfm').click(function(){
        $('#delArticlesForm').submit();
    });

    $('#delArticles').click(function () {
        if ($('.op_check').filter(':checked').size() > 0) {
            var articleIds = [];
            $('.op_check:checked').each(function(){
                articleIds.push($(this).val());
            });
            var articleIdsJson = JSON.stringify(articleIds);
            $('#articleIds').val(articleIdsJson);
            $('#delArtsCfmModel').modal();
        } else {
            $('#selArtsCfmModel').modal();
        }
    });
});

//JS For confirm to delete a comment in articleDetails page
function delCommentCfm(url) {
    $('#delCommentCfmClick').click(function(){
        window.location.href = url;
    });
    $('#delCommentCfmModel').modal();
}

//JS For select comments to delete

//function sub_JSON_data(commentIds) {
//    console.log(commentIds);
//    console.log(typeof commentIds);
//    $.ajax({
//        type:'post',
//        url:'manage-comments/delete-comments',
//        data: commentIds
//    });
//}
//注意，可以使用Ajax技术，但是批量删除评论的情况直接使用表单会简单，因为还需要考虑整个页面的处理

$(document).ready(function(){
    $('#delComments').click(function(){
        if($('.op_check_com').filter(':checked').size() > 0) {
            var commentIds = [];
            $('.op_check_com:checked').each(function(){
                commentIds.push($(this).val());
            });
            var commentIdsJson = JSON.stringify(commentIds);
            $('#commentIds').val(commentIdsJson);
            $('#delComsCfm').click(function() {
                $('#delCommentsForm').submit();
            });
            $('#delComsCfmModel').modal();
        } else {
            $('#selComsCfmModal').modal();
        }
    });
});

//JS For reply to a comment in manage-comments page
function pop_commentForm(followId, articleId) {
    $('#follow').val(followId);
    $('#article').val(articleId);
    $('#commentFormModel').modal();
}

//JS For add articleType
$(document).ready(function() {
    $('.add-articleType-btn').click(function() {
        $('#addArticleTypeFormModel').modal();
    });
});

//JS For confirm to delete an articleType
function delArticleTypeCfm(url) {
    $('#delArticleTypeCfmClick').click(function(){
        window.location.href = url;
    });
    $('#delArticleTypeCfmModel').modal();
}

//JS For edit articleType to get its info
function get_articleType_info(url, id, name, is_hide, introduction, menu_id) {
    $('#editName').val(name);
    $('#editSetting_hide').val(is_hide?'true':'false');
    $('#editIntroduction').val(introduction);
    $('#editMenus').val(menu_id?menu_id:-1);
    $('#articleType_id').val(id);
    $('#editArticleTypeForm').attr('action', url)
    $('#ModalTitle').text('修改博文分类：' + name);
    if (name == '未分类') {
        $('#editName').prop('readonly', true);
        $('#editIntroduction').prop('readonly', true);
    } else {
        $('#editName').prop('readonly', false);
        $('#editIntroduction').prop('readonly', false);
    }
    $('#editArticleTypeFormModel').modal();
}

//JS For add articleType
$(document).ready(function() {
    $('.add-articleType-nav-btn').click(function() {
        $('#addArticleTypeNavFormModel').modal();
    });
});

//JS For edit articleTypeNav to get its info
function get_articleTypeNav_info(url, id, name) {
    $('#editNavName').val(name);
    $('#nav_id').val(id);
    $('#editArticleTypeNavForm').attr('action', url)
    $('#NavModalTitle').text('修改分类导航：' + name);
    $('#editArticleTypeNavFormModel').modal();
}

//JS For confirm to delete an articleType nav
function delArticleTypeNavCfm(url) {
    $('#delArticleTypeNavCfmClick').click(function(){
        window.location.href = url;
    });
    $('#delArticleTypeNavCfmModel').modal();
}

//JS For editing blog info
function get_blog_info() {
    $('#editBlogInfoFormModal').modal();
}

//JS For confirm to delete a plugin
function delPluginCfm(url) {
    $('#delPluginCfmClick').click(function () {
        location.href = url
    });
    $('#delPluginCfmModal').modal();
}

//JS For change password
function changePassword() {
    $('#changePasswordFormModal').modal();
}

//JS For edit user info
function editUserInfo() {
    $('#editUserInfoFormModal').modal();
}

//js for checkDoublePassword
function checkChangePasswordForm() {
    var password = $('#password').val();
    var password2 = $('#password2').val();
    if (password != password2) {
        $('#group_password2').addClass('has-error');
        $('#password2_err').show();
        return false;
    } else {
        $('#changePasswordForm').submit();
        return true;
    }
}
