$(document).ready(function () {

    let href = $('#approve').attr('href');

    // budget
    $('#budget').on('input', function () {

        let budget = $(this).val();
        let new_href = href + `&budget=${budget}`;
        $('#approve').attr('href', new_href);

    });

    // budget_pass_date
    $('#budget_pass_date').on('change', function () {

        let date = $(this).val();
        let new_href = href + `&budget_pass_date=${date}`;
        $('#approve').attr('href', new_href);

    });

    // filter_company_id
    $('#filter_company_id').change(function () {
        $('#filter_requisition_id').val('');
        $('#filter_department').val('');
        $('#filter_status').val('');
    });

    // filter_department
    $('#filter_department').change(function () {
        $('#filter_requisition_id').val('');
        $('#filter_company_id').val('');
    });

    // filter_status
    $('#filter_status').change(function () {
        $('#filter_requisition_id').val('');
        $('#filter_company_id').val('');
    });

    $('#filter_requisition_id').on('input', function () {
        $('#filter_department').val('');
        $('#filter_status').val('');
        $('#filter_company_id').val('');
    });

});