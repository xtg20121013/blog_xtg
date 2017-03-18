function checkPasswordForm() {
    var password = $('#password').val();
    var password2 = $('#password2').val();
    if (password != password2) {
        $('#group_password2').addClass('has-error');
        $('#password2_err').show();
        return false;
    } else {
        // $('#changePasswordForm').submit();
        return true;
    }
}