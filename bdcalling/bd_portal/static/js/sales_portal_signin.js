$(document).ready(function () {

    // Show / hide login password
    $('#login_toggle_password').click(function () {
        var loginPassword = $('#login_password');
        $(this).removeClass();

        if (loginPassword.attr('type') === 'password') {
            loginPassword.attr('type', 'text')
            $(this).addClass('fas fa-eye');

        } else {
            loginPassword.attr('type', 'password');
            $(this).addClass('fas fa-eye-slash');
        }
    });

    // 

    
});