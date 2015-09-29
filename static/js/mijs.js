$('#sidebar').affix({
  offset: {
    top: $('#cabecera').height()
  }
});


$(document).ready(function(){
    // SELECCIONA TODO LOS CHECKBOX
    $('#todosLosCheck').click(function(event) {  //on click 
        if(this.checked) { // check select status
            $('.checkboxList').each(function() { //loop through each checkbox
                this.checked = true;  //select all checkboxes with class "checkboxList"               
            });
        }else{
            $('.checkboxList').each(function() { //loop through each checkbox
                this.checked = false; //deselect all checkboxes with class "checkboxList"                       
            });         
        }
    });

    $(window).scroll(function(){
        if ($(this).scrollTop() > 100) {
            $('.scrollup').fadeIn();
        } else {
            $('.scrollup').fadeOut();
        }
    });

    $('.scrollup').click(function(){
        $("html, body").animate({ scrollTop: 0 }, 600);
        return false;
    });


});


