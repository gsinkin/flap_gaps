function bind_echo_form() {
  $("#echo-form").submit(function() {
    $.post("https://flap-gaps.herokuapp.com/retort/echo",
           $(this).serialize(), function(data) {
             $("#response").text(data.result);
           }).fail(function(data) {
             $("#response").text($.parseJSON(data.responseText).result);
           });
     return false;
  });
};

$(document).ready(
  function () {
    bind_echo_form();
    $("#headline").css("color", "yellow");
  });
