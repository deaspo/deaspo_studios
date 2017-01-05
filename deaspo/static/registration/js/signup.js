/**
 * Created by polyc on 28/12/2016.
 */
$(document).ready(function () {
    $('#id_email').on('change paste', function (e) {
        if (!this.value) {
            alert("Blank email not allowed");
            this.focus();
            return false;
        } else {
            email = this.value;
            if (validateEmail(email)) {
                $('#email').val(email);
            } else {
                alert("Please enter a valid email");
                this.focus();
                return false;
            }
        }
    });
    //checks all input values of certain type
    /*$( "input[type='text']" ).change(function() {
  // Check input( $( this ).val() ) for validity here
    });*/
});