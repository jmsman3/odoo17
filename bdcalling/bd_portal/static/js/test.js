$(document).ready(function () {

    $("#btn1").click(function () {

        url = '/ajax/orm'

        $.ajax({
            url: url,
            type: 'POST',
            data: {
                sql: 'select * from product_template;',
                key2: 'value2'
            },
            success: function (response) {
                let result = JSON.parse(response)
                console.log('Result:', result);
            },
            error: function (xhr, status, error) {
                console.log('Error:', error);
            }
        });


    });

});