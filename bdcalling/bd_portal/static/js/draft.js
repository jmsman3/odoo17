$('#btn_create_new_client').click(function () {

    // Get data
    let a_mp_customer_fullname = $('#a_mp_customer_fullname').val();
    let a_client_user_name = $('#a_client_user_name').val();

    var data = {
        a_mp_customer_fullname: 'a',
        a_client_user_name: 'aa',
    };

    // Parameters
    var url = "/ajax/create_new_client";
    var method = "POST";
    var jsonString = JSON.stringify(data);

    // Call json request
    $.ajax({
        url: url,
        type: method,
        data: jsonString,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (response) {
            console.log('success');
            console.log(response);
        },
        error: function (xhr, status, error) {
            console.log('error');
            console.log(xhr.responseText);
        }
    });

});

// ===================================================
[
    {
        "id": 85,
        "client_user_name": "client1",
        "name": "client1",
        "email": "client1@test.com",
        "phone": "01700000000",
        "mp_customer_fullname": "client 1"
    },
    {
        "id": 89,
        "client_user_name": "client2",
        "name": "client2",
        "email": "client2@test.com",
        "phone": "01700112233",
        "mp_customer_fullname": "Client 2"
    },
    {
        "id": 86,
        "client_user_name": "client2",
        "name": "client2",
        "email": "client2@test.com",
        "phone": "01711111111",
        "mp_customer_fullname": "client 2"
    },
    {
        "id": 87,
        "client_user_name": "client3",
        "name": "client3",
        "email": "client3@t.com",
        "phone": "01711223344",
        "mp_customer_fullname": "client 3"
    },
    {
        "id": 88,
        "client_user_name": "client4",
        "name": "client4",
        "email": "client4@t.com",
        "phone": "01731001896",
        "mp_customer_fullname": "client 4"
    },
    {
        "id": 90,
        "client_user_name": "client5",
        "name": "client5",
        "email": "client5@test.com",
        "phone": "01700112234",
        "mp_customer_fullname": "Client 5"
    },
    {
        "id": 106,
        "client_user_name": "client6",
        "name": "client6",
        "email": false,
        "phone": false,
        "mp_customer_fullname": false
    }
]