/* spinner: instantiate */
var opts = {
  lines: 13, // The number of lines to draw
  length: 20, // The length of each line
  width: 10, // The line thickness
  radius: 30, // The radius of the inner circle
  corners: 1, // Corner roundness (0..1)
  rotate: 0, // The rotation offset
  direction: 1, // 1: clockwise, -1: counterclockwise
  color: '#000', // #rgb or #rrggbb or array of colors
  speed: 1, // Rounds per second
  trail: 60, // Afterglow percentage
  shadow: false, // Whether to render a shadow
  hwaccel: false, // Whether to use hardware acceleration
  className: 'search-results', // The CSS class to assign to spinner
  zIndex: 2e9, // The z-index (defaults to 2000000000)
  top: '50px', // Top position relative to parent in px
  left: 'auto' // Left position relative to parent in px
};
var target = document.getElementById('alert-container');
var spinner = new Spinner(opts).spin(target);
spinner.stop(target);

$(function() {
  /* datepicker */
  $('input[id^="id_date"]').datepicker({
    firstDay:0,
    maxDate: new Date,
    changeFirstDay:false,
    dateFormat:'yy-mm-dd',
    buttonImage:'//www.carthage.edu/themes/shared/img/ico/calendar.gif',
    showOn:'both',
    buttonImageOnly:true
  });
  /* datatables initialization */
  var redpandaTable = $('#data-table').DataTable({
    'lengthMenu': [
      [100, 250, 500, 1000, 2000, -1],
      [100, 250, 500, 1000, 2000, 'All']
    ],
    'language': {
      'search': 'Filter records:',
      'lengthMenu': 'Display _MENU_'
    },
    drawCallback: function() {
      spinner.stop(target);
    },
    fixedHeader: true,
    order: [[2, 'desc']],
    dom: 'lfrBtip',
    responsive: true,
    buttons: [
      {
        extend: 'excelHtml5',
        exportOptions: {
          columns: ':visible'
        }
      }
    ]
    /*
    serverSide: true,
    pageLength=25,
    ajax: {
       url: '{% url %}',
       'type': 'post',
       dataSrc: function ( json ) {
         return json;
       },
       beforeSend: function(){
         spinner.spin(target);
       },
       success: function(data) {
         spinner.stop(target);
       }
    },
    "columns": [
        {
            'data': 'created_by',
            'render': function(data, type, row){
                return $("<div>").append($("<a/>").attr("href", "mailto:" + row.created_by + "/").text(data)).html();
            }
        },
        { 'data': 'cid' },
        { 'data': 'created_at' },
        { 'data': 'tested_positive' },
        { 'data': 'tested_negative' },
        { 'data': 'tested_pending' },
        { 'data': 'negative' },
        { 'data': 'temperature' },
        { 'data': 'cough' },
        { 'data': 'loss_taste_smell' },
        { 'data': 'sore_throat' },
        { 'data': 'congestion' },
        { 'data': 'fatigue' },
        { 'data': 'body_aches' },
        { 'data': 'headache' },
        { 'data': 'nausea' },
        { 'data': 'diarrhea' },
        { 'data': 'quarantine'},
        { 'data': 'notification'}
    ]
    */
  });
  /* clear django cache object by cache key and refresh content */
  $('.clear-cache').on('click', function(e){
    e.preventDefault();
    var $dis = $(this);
    var $cid = $dis.attr('data-cid');
    var $target = '#' + $dis.attr('data-target');
    var $html = $dis.html();
    $dis.html('<i class="fa fa-refresh fa-spin"></i>');
    $.ajax({
      type: 'POST',
      url: $clearCacheUrl,
      data: {'cid':$cid},
      success: function(data) {
        $.growlUI("Cache", "Clear");
        $($target).html(data);
        $dis.html('<i class="fa fa-refresh"></i>');
      },
      error: function(data) {
        $.growlUI("Error", data);
      }
    });
    return false;
  });
  /* override the submit event for the alert form to handle some things */
  $('form#health-check').submit(function(){
    // disable submit button after users clicks it
    $(this).children('input[type=submit]').attr('disabled', 'disabled');
  });
});
