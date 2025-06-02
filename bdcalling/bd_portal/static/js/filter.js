$(document).ready(function () {

    // Show the dropdown when the input is focused
    $("#f_query").focus(function () {
        $("#query_sugg").show();
    });

    // Hide the dropdown when clicking outside of the input or dropdown
    $(document).click(function (event) {
        if (!$(event.target).closest("#f_query, #query_sugg").length) {
            $("#query_sugg").hide();
        }
    });

    // Optional: keep the dropdown visible when clicking inside it
    $("#query_sugg").click(function (event) {
        event.stopPropagation();
    });

    // Clear suggestions on subject change
    $('#f_query_for').change(function () {
        $('#query_sugg').empty();
    });

    $('#f_query').keyup(function () {

        $('#query_sugg').empty();

        let query = $(this).val();
        console.log(query);

        let url = '';
        let code = $('#f_query_for').val();

        if (code == 'sales_employee') {
            url = "/f_sales_employee_id";

        } else if (code == 'platform_source') {
            url = "/f_platform_source";

        } else if (code == 'order_source') {
            url = "/f_order_source";

        } else if (code == 'profile_name') {
            url = "/f_profile_id";

        } else if (code == 'client_name') {
            url = "/f_client_user_id";

        } else if (code == 'order_id') {
            url = "/f_order_id";
        }

        $.post(url,

            {
                query: query,
                city: "Dhaka"
            },

            function (data, status) {

                if (status == 'success') {

                    let response = JSON.parse(data);
                    $('#query_sugg').empty();

                    let html = `
                    <div class="list-group">`;

                    if (response.data) {
                        response.data.forEach((item) => {

                            html += `
                            <a href="${item.url}" class="list-group-item list-group-item-action">${item.name}</a>
                            `;

                        });
                    }

                    html += `</div>`;

                    $('#query_sugg').append(html);
                    console.log(response);

                }

            }
        );

    });

    // Submit on status change
    $('#filter_order_status').on('change', function () {

        let status = $(this).val();
        if (status.length > 0) {
            $('#form_filter').submit();
        }

    });

});