$(document).ready(function(){
    var priceArray = $('.price').map(function(){
        return $(this).text();
    }).get();
    
    var total = 0;
    for (var i = 0; i < priceArray.length; i++){
        total += parseInt(priceArray[i]);
    }
    
    $('#grand_total').text(parseFloat(total).toFixed(2));

    $('#form_toggler').click(function(){
        $('.contact_form').toggle(500);
    });
});

