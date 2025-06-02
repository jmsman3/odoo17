$(document).ready(function () {
    $("#image_1920").change(function (e) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#preview_image').attr('src', e.target.result);
            $('#preview_image').show();
        };
        reader.readAsDataURL(e.target.files[0]);
    });
});
