$(function(){

    $(".toggle-password").click(function() {

        $(this).toggleClass("eye");
        var input = $($(this).attr("toggle"));
        if (input.attr("type") == "password") {
          input.attr("type", "text");
        } else {
          input.attr("type", "password");
        }
      });
})


