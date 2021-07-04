$(document).ready(function(){

  $('.fa-bars').click(function(){
    $(".sidenav").addClass('show');
    $('body').addClass('overflow-hide');
  });  

  $('.sidenav').click(function(event){
    if(!$(event.target).closest(".sidebar").length){
      $(".sidenav").removeClass('show');
      $('body').removeClass('overflow-hide');
    }
  });

  
  $('#product-item').click(function(){
    $('#product-item-menu').toggle()
    $('#product-item').toggleClass('list-group-item-action')
  });

  $('#order-item').click(function(){
    $('#order-item-menu').toggle()
    $('#order-item').toggleClass('list-group-item-action')
  });

  // Manage Stock Data Table Code
  $('#stock_data').DataTable({
    "ordering": false,
    "scrollX": true,
  });

  // Search Item in Order
  $("#search").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#sort_data tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });

});
