$(document).ready(function () {
    // Invert the table
    $("tbody").each(function (elem, index) {
        var arr = $.makeArray($("tr", this).detach());
        arr.reverse();
        $(this).append(arr);
    });
    // Setup - add a text input to each footer cell
    $('#main_table thead tr')
        .clone(true)
        .addClass('filters')
        .appendTo('#main_table thead');
    
    var table = $('#main_table').DataTable({
        scrollX: true,
        fixedHeader: true,
        autoWidth: false,
        orderCellsTop: true,
        fixedHeader: true,
        aLengthMenu: [
            [10, 25, 50, 100, 200, -1],
            [10, 25, 50, 100, 200, "All"]
        ],
        iDisplayLength: 10,
     initComplete: function () {
            var api = this.api();
 
            // For each column
            api
                .columns()
                .eq(0)
                .each(function (colIdx) {
                    // Set the header cell to contain the input element
                    var cell = $('.filters th').eq(
                        $(api.column(colIdx).header()).index()
                    );
                    var title = $(cell).text();
                    $(cell).html('<input type="text" placeholder="' + title + '" />');
 
                    // On every keypress in this input
                    $(
                        'input',
                        $('.filters th').eq($(api.column(colIdx).header()).index())
                    )
                        .off('keyup change')
                        .on('change', function (e) {
                            // Get the search value
                            $(this).attr('title', $(this).val());
                            var regexr = '({search})'; //$(this).parents('th').find('select').val();
 
                            var cursorPosition = this.selectionStart;
                            // Search the column for that value
                            api
                                .column(colIdx)
                                .search(
                                    this.value != ''
                                        ? regexr.replace('{search}', '(((' + this.value + ')))')
                                        : '',
                                    this.value != '',
                                    this.value == ''
                                )
                                .draw();
                        })
                        .on('keyup', function (e) {
                            e.stopPropagation();
 
                            $(this).trigger('change');
                            $(this)
                                .focus()[0]
                                .setSelectionRange(cursorPosition, cursorPosition);
                        });
                });
            // Recalculate column widths after building filter row (fix header/body misalignment with scrollX)
            setTimeout(function(){
                api.columns.adjust();
            }, 0);
        },
    });
    // Keep header/body column widths aligned with scrollX on various events
    table.columns.adjust();
    $(window).on('resize.dt', function(){dataTables_filter
        table.columns.adjust();
    });
    table.on('column-visibility.dt draw.dt responsive-resize.dt', function(){
        table.columns.adjust();
    });
});
