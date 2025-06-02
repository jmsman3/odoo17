$(document).ready(function () {

    $('#req_att_files').on('change', function () {

        var files = $(this)[0].files; // Get selected files

        // Iterate through each selected file and append its name to the div
        let att_html = '';

        for (var i = 0; i < files.length; i++) {
            att_html += `<li class="list-group-item">${files[i].name}</li>`;
        }

        $('#con_req_att_list').show();
        $('#req_att_list').html(att_html);

    });

    $('#req_ap_att_files').on('change', function () {

        var files = $(this)[0].files; // Get selected files

        // Iterate through each selected file and append its name to the div
        let att_html = '';

        for (var i = 0; i < files.length; i++) {
            att_html += `<li class="list-group-item">${files[i].name}</li>`;
        }

        $('#con_req_ap_att_list').show();
        $('#req_ap_att_list').html(att_html);

    });

    // Product lines
    let product_lines = [];
    let product_line_id = 1;

    $('#p_line_add_product').click(function () {

        let product_line = {
            id: product_line_id,
            product_id: '',
            description: '',
            quantity: 1,
            purpose_of_use: ''
        }

        product_lines.push(product_line);

        let product_line_html = `
            <!-- Product line -->
            <tr id="tr_product_line_${product_line_id}">
                <td>
                    <input id="search_${product_line_id}" class="input search" type="text" data_id="${product_line_id}" placeholder="Search Product" />

                    <div class="c_query_sugg">

                        <div id="query_sugg_id_${product_line_id}" class="query_sugg" style="display: none2" class="w-100">
                            <!-- Dynamic content -->
                        </div>

                    </div>  

                </td>
                <td>
                    <input class="input line_item" type="text" data_id="${product_line_id}" data_name="description" placeholder="Description" />
                </td>
                <td>
                    <input class="input line_item line_item_quantity" type="number" min="1" data_id="${product_line_id}" data_name="quantity" value="1" placeholder="Quantity" />
                </td>
                <td>
                    <input class="input line_item" type="text" data_id="${product_line_id}" data_name="purpose_of_use" placeholder="Purpose of Use" />
                </td>
                <td>
                    <button type="button" class="btn btn-danger remove_product_line" data_id="${product_line_id}">Remove</button>
                </td>
            </tr>
            <!-- End Product line -->
        `;

        product_line_id += 1;

        $('#tbl_product_line').append(product_line_html);

    });

    // Remove product line
    $(document).on('click', '.remove_product_line', function (e) {
        let data_id = $(this).attr('data_id');
        $(`#tr_product_line_${data_id}`).remove();

        // Update product_lines array
        product_lines.forEach((item, index) => {
            if (item.id == data_id) {
                product_lines.splice(index, 1)
            }
        })

        console.log(product_lines);

    })

    // Remove product line
    $(document).on('keyup', '.line_item', function (e) {

        let data_id = $(this).attr('data_id');
        let data_name = $(this).attr('data_name');
        let type = $(this).attr('type');
        let val = $(this).val();

        // Update product_lines array
        product_lines.forEach((item, index) => {

            if (item.id == data_id) {

                if (type == 'number') {
                    item[data_name] = parseInt(val);

                } else {
                    item[data_name] = val;
                }

            }
        })

        console.log(product_lines);

    })

    /* ========================================================== */
    let sel_line_id = null;

    // Show the dropdown when the input is focused
    $(document).on('focusin', '.search', function () {
        $('.query_sugg').hide();
        let data_id = $(this).attr('data_id');
        $(`#query_sugg_id_${data_id}`).show();
    })

    $(document).click(function (event) {

        if (event.target.classList.contains('search')) {

        } else {
            $('.query_sugg').hide();
        }

    });

    $(document).on('keyup', '.search', function () {
        let data_id = $(this).attr('data_id');
        let val = $(this).val();
        sel_line_id = data_id
        let timeout = null;

        clearTimeout(timeout);

        timeout = setTimeout(function () {
            ajaxGetProducts();
        }, 100);

        function ajaxGetProducts() {
            let url = '/ajax_requisition_get_products';
            let query = val;
            $.post(url,

                {
                    query: query,
                    city: "Dhaka"
                },

                function (data, status) {

                    if (status == 'success') {

                        let response = JSON.parse(data);

                        if (response.status == 'success') {

                            let products = response.data;

                            $(`#query_sugg_id_${sel_line_id}`).empty();

                            let sugg_html_items = ``;

                            products.forEach((item, index) => {
                                sugg_html_items += `<li class="list-group-item list-group-item-action sugg_product" 
                            data_line_id="${sel_line_id}" data_product_id="${item.id}">${item.name}</li>`;
                            })

                            let sugg_html = `
                        <ul class="list-group">
                            ${sugg_html_items}
                        </ul>
                        `;

                            $(`#query_sugg_id_${sel_line_id}`).html(sugg_html);
                        }

                    }

                }
            );
        } // End ajaxGetProducts

    }) // End keyup, .search

    // When click on suggested product
    $(document).on('click', '.sugg_product', function () {

        let data_product_id = $(this).attr('data_product_id');
        let data_line_id = $(this).attr('data_line_id');
        let text = $(this).text();
        $(`#search_${data_line_id}`).attr('data_product_id', data_product_id);
        // $(`#search_${data_line_id}`).val(text);
        $(`#search_${data_line_id}`).val(text).trigger('change');

    });

    // When click on suggested product
    $(document).on('change', '.search', function () {
        console.log('search changed');
        let data_product_id = $(this).attr('data_product_id')
        console.log(data_product_id);

        let data_id = $(this).attr('data_id');
        let type = $(this).attr('type');

        // Update product_lines array
        product_lines.forEach((item, index) => {

            if (item.id == data_id) {
                item['product_id'] = data_product_id;
            }

        })

        console.log('product_lines', product_lines);

    });

    // Submit
    $('#requisition').submit(function (e) {

        console.log('Submitted');
        let error = false;

        const allProductIdsValid = product_lines.every(product => {
            if (product.product_id === "") {
                error = true;
                return false;  // Causes `every()` to stop and return false
            }
            return true;
        });

        if (!allProductIdsValid) {
            error = true;
            e.preventDefault();
            alert('One or more products have an invalid product_id.');
            return;
        }

        let product_lines_json = JSON.stringify(product_lines);
        $('#product_lines').val(product_lines_json);

        if (error) {
            e.preventDefault();
        }

    });


});
