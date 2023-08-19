var date_range = null;

function generate_report() {
    // crea un nuevo objeto `Date`
    var today = new Date();

    // `getDate()` devuelve el día del mes (del 1 al 31)
    var day = today.getDate();

    // `getMonth()` devuelve el mes (de 0 a 11)
    var month = today.getMonth() + 1;

    // `getFullYear()` devuelve el año completo
    var year = today.getFullYear();

    // muestra la fecha de hoy en formato `MM/DD/YYYY`
    hoy = year + '-' + month + '-' + day;

    var parameters = {
        'action': 'search_report',
        'start_date': hoy,
        'end_date': hoy,
    };

    if (date_range !== null) {
        parameters['start_date'] = date_range.startDate.format('YYYY-MM-DD')
        parameters['end_date'] = date_range.endDate.format('YYYY-MM-DD')
        table.destroy();
    }

    table = $('#data').DataTable({
        paging: false,
        searching: false,

        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: parameters,
            dataSrc: ''

        },
        dom: 'Bfrtip',
        buttons: [
            'excel', 'pdf'
        ],
        columns: [
            { "data": "claveCatastral_id" },
            { "data": "formaPago_id" },
            { "data": "agnio" },
            { "data": "recargo" },
            { "data": "descuento" },
            { "data": "fechaPago" },
            { "data": "total" },
        ],

        columnDefs: [{
            targets: [3, 4, 6],
            class: 'text-center',
            orderable: false,
            render: function(data, type, row) {
                return '$' + parseFloat(data).toFixed(2);
            }
        }],


    })



}


$(function() {

    $('input[name="date_range"]').daterangepicker(

    ).on('apply.daterangepicker', function(ev, picker) {
        date_range = picker;
        console.log(picker.startDate.format('MM/DD/YYYY') + ' - ' + picker.endDate.format('MM/DD/YYYY'));
        generate_report()

    });
    generate_report()

});