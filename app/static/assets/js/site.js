$(document).ready(function(){
  //alert('Hello World!');
    $("#affirmationForm").hide();

    $('#affirmationButton').click(function(){
        $("#affirmationForm").toggle();
    });

    onChange="this.form.submit()"
});



