$(function() {
  $("#id_negative").on('change', function() {
    if(this.checked) {
      $('input[type="checkbox"]').not(this).prop("checked", false);
    }
  });
  $('input[type="checkbox"]').bind('click',function() {
    if ($(this).attr('id') != 'id_negative') {
      $("#id_negative").prop("checked", false);
    };
  });
  /* override the submit event for the alert form to handle some things */
  $('form#health-check').submit(function(){
    // disable submit button after users clicks it
    $(this).children('input[type=submit]').attr('disabled', 'disabled');
  });
});
