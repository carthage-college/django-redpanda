function set_icon(check){
    icon = '';
    if (check == true) {
        icon = '<i class="fa fa-check green" title="Tested Positive"><span style="display:none;">x</span></i>';
    }
    return icon;
}

$(function(){
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
  /* datatables initialization for managers */
  $('#redpandaManagers').DataTable({
    'lengthMenu': [
      [100, 250, 500, 1000, 2000, 5000, 10000],
      [100, 250, 500, 1000, 2000, 5000, 10000]
    ],
    'language': {
      'search': 'Filter records:',
      'lengthMenu': 'Display _MENU_'
    },
    order: [[3, 'desc']],
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
  });
  /* datatables initialization for administrators */
  $('#redpandaAdmins').DataTable({
    'lengthMenu': [
      [100, 250, 500, 1000, 2000, 0],
      [100, 250, 500, 1000, 2000, 'All']
    ],
    'language': {
      'search': 'Filter records:',
      'processing': '<i class="fa fa-spinner fa-spin fa-4x fa-fw"></i><span class="sr-only">Loading...</span>',
      'lengthMenu': 'Display _MENU_'
    },
    order: [[3, 'desc']],
    dom: 'lfrBtip',
    buttons: [
      {
        extend: 'excelHtml5',
        exportOptions: {
          columns: ':visible'
        }
      }
    ],
    //destroy: true,
    responsive: true,
    serverSide: true,
    processing: true,
    paging: true,
    pageLength: 100,
    ajax: {
       'url': $homeAjaxUrl,
       'type': 'post',
       'processData': true,
       'dataType': 'json',
       // debugging
       //dataFilter: function(reps) {
         //console.log(reps);
         //return reps;
       //},
       //error: function(err){
         //console.log(err);
       //},
       'data': {
            'date_start': $dateStart,
            'date_end': $dateEnd,
            'sport': $sport,
            'group': $group,
            'csrfmiddlewaretoken': $csrfToken
       }
    },
    'columns': [
        {
          'data': 'full_name',
          'className': 'full_name',
          'render': function(data, type, row){
              return $("<div>").append($("<a/>").attr("href", "mailto:" + row.email + "/").text(data)).html();
          }
        },
        {
            'data': 'vaccine',
            'searchable': false,
            'render': function(data, type, row){
                return set_icon(data);
            }
        },
        { 'data': 'cid' },
        {
            'data': 'created_at',
            'searchable': false,
            'className': 'created_at'
        },
        {
            'data': 'group',
            'className': 'group',
            'searchable': false,
            'orderable': false
        },
        {
            'data': 'tested_positive',
            'searchable': false,
            'render': function(data, type, row){
                return set_icon(data);
            }
        },
        {
            'data': 'tested_negative',
            'searchable': false,
            'render': function(data, type, row){
                return set_icon(data);
            }
        },
        {
            'data': 'tested_pending',
            'searchable': false,
            'render': function(data, type, row){
                return set_icon(data);
            }
        },
        {
            'data': 'negative',
            'searchable': false,
            'render': function(data, type, row){
                return set_icon(data);
            }
        },
        {
            'data': 'temperature',
            'searchable': false,
            'render': function(data, type, row){
                return set_icon(data);
            }
        },
        {
            'data': 'cough',
            'searchable': false,
            'render': function(data, type, row){
                return set_icon(data);
            }
        },
        {
            'data': 'short_breath',
            'searchable': false,
            'render': function(data, type, row){
                return set_icon(data);
            }
        },
        {
            'data': 'loss_taste_smell',
            'searchable': false,
            'render': function(data, type, row){
                return set_icon(data);
            }
        },
        {
            'data': 'sore_throat',
            'searchable': false,
            'render': function(data, type, row){
                return set_icon(data);
            }
        },
        {
            'data': 'congestion',
            'searchable': false,
            'render': function(data, type, row){
                return set_icon(data);
            }
        },
        {
            'data': 'fatigue',
            'searchable': false,
            'render': function(data, type, row){
                return set_icon(data);
            }
        },
        {
            'data': 'body_aches',
            'searchable': false,
            'render': function(data, type, row){
                return set_icon(data);
            }
        },
        {
            'data': 'headache',
            'searchable': false,
            'render': function(data, type, row){
                return set_icon(data);
            }
        },
        {
            'data': 'nausea',
            'searchable': false,
            'render': function(data, type, row){
                return set_icon(data);
            }
        },
        {
            'data': 'diarrhea',
            'searchable': false,
            'render': function(data, type, row){
                return set_icon(data);
            }
        },
        {
            'data': 'quarantine',
            'searchable': false,
            'render': function(data, type, row){
                return set_icon(data);
            }
        }
    ]
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
});
