$(document).ready(function () {

    function copyToClipboard(text) {
        var tempInput = $('<input>');
        $('body').append(tempInput);
        tempInput.val(text).select();
        document.execCommand('copy');
        tempInput.remove();
        // alert('Copied to clipboard: ' + text);
    }

    $('#svg_copy').click(function () {
        var orderLink = $('#order_link').val();
        copyToClipboard(orderLink);

    });

    /*
        This script calculates and displays the remaining time until the delivery date
        specified in the input field with id "delivery_last_date".
        It updates the remaining time every second.
    */
    function updateRemainingTime() {

        var deliveryDateRaw = $("#delivery_last_date").val();
        console.log(deliveryDateRaw);
        deliveryDateRaw = deliveryDateRaw.replaceAll('T', ' ');

        // var deliveryDate = new Date(`${deliveryDateRaw} 24:00:00`);
        var deliveryDate = new Date(`${deliveryDateRaw}:00`);  // Later

        if (deliveryDate == 'Invalid Date') {
            return;
        }

        var currentDate = new Date();

        var timeDifference = deliveryDate.getTime() - currentDate.getTime();

        var days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
        var hours = Math.floor((timeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((timeDifference % (1000 * 60)) / 1000);

        if (seconds < 0) {
            // var remainingTime = `<div> ${days}D | ${hours}H | ${minutes}M | ${seconds}S <span class="text-danger">Late delivery</span> </div>`;
            var remainingTime = `<div><span class="text-danger">Late delivery</span></div>`;
        } else {
            var remainingTime = `<div> ${days}D | ${hours}H | ${minutes}M | ${seconds}S</div>`;
        }

        $("#remaining_time").html(remainingTime);
    }

    // Call the function initially to set the remaining time
    updateRemainingTime();

    // Update remaining time every second
    let tmrUpdateRemainingTime = setInterval(updateRemainingTime, 1000);

    $('#amount').keyup(function () {
        //        let amount = parseInt($(this).val());
        //        let per = parseInt($('#percentage').val());
        //        let one_per = amount / 100;
        //        let per_amount = one_per * per;
        //        let charges_amount = amount * per_amount;
        //        let delivery_amount = amount - charges_amount;
        //
        //        // Format 'a' to display two digits after the decimal point
        //        let f_charges_amount = charges_amount.toFixed(2);
        //        let f_delivery_amount = delivery_amount.toFixed(2);
        //
        //        $('#charges_amount').val(f_charges_amount);
        //        $('#delivery_amount').val(f_delivery_amount);
    });

    /*
        Project Information
    */
    let project_info_switch = "off";
    let iv = '';
    let server_data = JSON.parse($('#js_server_data').val());
    let employee = server_data.employee;

    $('#project_info_switch').mouseup(function () {

        if (project_info_switch == 'off') {

            project_info_switch = 'on';
            $('#operation_employee_id').val(employee.id);
            $('#operation_employee_id_barcode').val(employee.barcode);
            $('#operation_employee_name').val(employee.name);

        } else {

            project_info_switch = 'off';
            $('#operation_employee_id').val('');
            $('#operation_employee_id_barcode').val('');
            $('#operation_employee_name').val('');

        }

        console.log(employee);

    });

    // Operation Employee ID auto fill
    // let js_employees = $('#js_employees').val();
    // let employees = JSON.parse(js_employees);
    // $('#operation_employee_id_barcode').on('input', function () {

    //     let thisVal = $(this).val();

    //     $('#operation_employee_name').val('');

    //     employees.forEach((element) => {

    //         if (thisVal == element.barcode) {

    //             $('#operation_employee_id').val(element.id);

    //             if (element.name) {
    //                 $('#operation_employee_name').val(element.name);
    //             }

    //             is_operation_employee_id = true;  // Can be use for submit validation
    //             console.log(element);

    //         }
    //     })

    // });

    /*
    Platform Source and profile
    */
    let _json_all_profiles = $('#json_all_profiles').val();
    let json_all_profiles = JSON.parse(_json_all_profiles);

    // On change
    $('#platform_source').change(function () {

        let platform_source_id = $(this).val();
        $('#profile_name').empty();

        let html_profiles = ``;

        json_all_profiles.forEach((item, index) => {

            if (item.platform_source_id == platform_source_id) {

                html_profiles += `<option value="${item.id}">${item.name}</option>\n`;

            }

        })

        $('#profile_name').append(html_profiles);

    });
    /*
    End Platform Source and profile
    */

    /*
        client_user_id on change
    */
    let js_clients = $('#js_clients').val();
    let clients = JSON.parse(js_clients);

    console.log('clients');
    console.log(clients);

    $('#client_user_id').on('input', function () {

        let thisVal = $(this).val();
        $('.group_client').val('');
        is_client_user_name = false;
        $('#hidden_client_user_id').val('');

        clients.forEach((element) => {

            if (thisVal == element.client_user_name) {

                if (element.mp_customer_fullname) {
                    $('#client_name').val(element.mp_customer_fullname);

                }

                if (element.email) {
                    $('#client_email').val(element.email);

                }

                if (element.phone) {
                    $('#client_phone').val(element.phone);

                }

                is_client_user_name = true;
                $('#hidden_client_user_id').val(element.id);

            }
        });

    });

    /*
        End client_user_id on change
    */

    //btn_create_new_client
    $('#btn_create_new_client').click(function () {

        // Clear form
        function clear_form() {
            $('#a_client_user_name').val('');
            $('#a_mp_customer_fullname').val('');
            $('#a_street').val('');
            $('#a_city').val('');
            $('#a_zip').val('');
            $('#a_country_id').val('');
            $('#a_phone').val('');
            $('#a_email').val('');
            $('#a_website').val('');
        }

        // Init Reset
        $('#alert').empty();
        $('#alert').hide();
        $('#alert_success').empty();
        $('#alert_success').hide();

        // Get data
        let client_user_name = $('#a_client_user_name').val();
        let mp_customer_fullname = $('#a_mp_customer_fullname').val();
        let street = $('#a_street').val();
        let city = $('#a_city').val();
        let zip = $('#a_zip').val();
        let country_id = $('#a_country_id').val();
        let phone = $('#a_phone').val();
        let email = $('#a_email').val();
        let website = $('#a_website').val();

        // At least one char
        const regex = /[a-zA-Z]/;
        client_user_name = client_user_name.trim()

        if (!regex.test(client_user_name)) {
            alert('Please enter a valid client user name');
            return;
        }

        // Request parameters
        let url = "/ajax/create_new_client"
        var data = {
            client_user_name: client_user_name,
            mp_customer_fullname: mp_customer_fullname,
            street: street,
            city: city,
            zip: zip,
            country_id: country_id,
            phone: phone,
            email: email,
            website: website,
        };

        // Post Request
        $.post(url,
            data,
            function (data, status) {

                // alert("Data: " + data + "\nStatus: " + status);

                let result = JSON.parse(data);
                console.log(result);

                if (result.status == 'error') {

                    let error_html = ``;
                    error_html += `<li>${result.error.message}</li>`;
                    $('#alert').html(error_html);
                    $('#alert').show();

                } else if (result.status == 'success') {

                    console.log('success');

                    let client_values = {
                        "id": result.data.client.id,
                        "client_user_name": result.data.client.client_user_name,
                        "name": 'zzz',
                        "email": result.data.client.email,
                        "phone": result.data.client.phone,
                        "mp_customer_fullname": result.data.client.mp_customer_fullname,
                    }

                    clients.push(client_values);
                    console.log(clients);

                    let alert_success_html = ``;
                    alert_success_html += `<li>${result.message}</li>`;
                    $('#alert_success').html(alert_success_html);
                    $('#alert_success').show();
                    clear_form();

                    $('#client_user_id').val(result.data.client.client_user_name);
                    $('#client_user_id').trigger('input');

                }
            }
        );

    });

    /*
    js_server_data
    Global server data js object
*/
    // let js_server_data = $('#js_server_data').val();
    // let server_data = JSON.parse(js_server_data);

    $('#service_type_id').change(function () {

        let thisVal = parseInt($(this).val());
        $('#amount').val('');

        let service_types = server_data.service_types;
        service_types.forEach((element) => {

            if (thisVal == element.id) {

                $('#amount').val(element.unit_price);

            }
        })

        order_amount_cal();

    });

    /*
        Amount calculation
        Amount calculation
    */

    function order_amount_cal() {

        let amount = parseFloat($('#amount').val());
        let percentage = parseInt($('#percentage').val());
        let charges_amount = (percentage / 100) * amount;
        charges_amount = charges_amount.toFixed(2);  // New
        let delivery_amount = amount - charges_amount;
        delivery_amount = delivery_amount.toFixed(2);  // New

        $('#charges_amount').val(charges_amount);
        $('#delivery_amount').val(delivery_amount);
    }

    $('#amount').keyup(function () {
        order_amount_cal();
    });

    $('#percentage').change(function () {
        order_amount_cal();
    });

    /* -------------------------------------------------------- */
    let js_employees = $('#js_employees').val();
    let employees = JSON.parse(js_employees);

    function getEmployeeByCode(this_val) {

        let thisVal = this_val;
        $('.group_sales_employee').val('');
        $('#hidden_sales_employee_id').val('');
        is_sales_employee_id = false;

        employees.forEach((element) => {

            if (thisVal == element.barcode) {

                if (element.name) {
                    $('#sales_employee_name').val(element.name);
                }

                if (element.company_name) {
                    $('#sales_employee_company_name').val(element.company_name);
                }

                $('#hidden_sales_employee_id').val(element.id);
                is_sales_employee_id = true;

            }
        })
    }

    // let employee = server_data.employee;
    let employee_switch = "off";
    let order_emp_barcode = $('#sales_employee_id').val();

    $('#employee_switch').mouseup(function () {

        if (employee_switch == 'off') {

            employee_switch = 'on';
            let employee_barcode = $('#employee_id').val();
            $('#sales_employee_id').val(employee_barcode);
            $('#sales_employee_id').trigger('input');
            $('.group_sales_employee_text').attr('disabled', '1');

        } else {

            employee_switch = 'off';
            $('#sales_employee_id').val(order_emp_barcode);
            $('#sales_employee_id').trigger('input');
            // $('.group_sales_employee_text').val('');
            $('.group_sales_employee_text').removeAttr('disabled');
        }

    });

    $('#sales_employee_id').on('input', function () {
        let this_val = parseInt($(this).val());
        getEmployeeByCode(this_val);
    });
    /* -------------------------------------------------------- */


});