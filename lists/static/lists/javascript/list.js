jQuery(document).ready(function($) {
   //on typing in the input field, want to hide the error field
   $('input[name="text"]').on('keypress', function() {
        $('.has-error').hide();
    });
});