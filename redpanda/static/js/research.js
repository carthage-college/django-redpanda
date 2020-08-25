$(function() {
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
        //$.growlUI("Cache", "Clear");
        alert('Cache Cleared');
        $($target).html(data);
        $dis.html('<i class="fa fa-refresh"></i>');
      },
      error: function(data) {
        //$.growlUI("Error", data);
        alert('Error:' + data);
      }
    });
    return false;
  });

  $('input[name="smellCorrect"]').click(function(){
    $('.smellLoss').toggleClass(
      'show', $('input[name="smellCorrect"]:checked').length <= 5
    );
  });
  $('input[name="customID"]').val(Math.random().toString(36).substring(2, 8) + Math.random().toString(36).substring(2, 8));
  /* override the submit event for the alert form to handle some things */
  $('form#smell-test').submit(function(){
    // disable submit button after users clicks it
    $(this).children('input[type=submit]').attr('disabled', 'disabled');
  });
});
