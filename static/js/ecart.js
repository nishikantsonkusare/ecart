$(document).ready(function(){
  $('.fa-bars').click(function(){
    $(".sidenav").toggle(300);
    $('body').addClass('overflow-hide');
  });  

  $('.sidenav').click(function(event){
    if(!$(event.target).closest(".sidebar").length){
      $(".sidenav").toggle(300);
      $('body').removeClass('overflow-hide');
    }
  });

// Home page Feature Product Carousel
var owl = $('#feature_product');
  // 
  owl.owlCarousel({
    margin:10,
    dots: false,
    autoplay: true,
    autoplayTimeout: 5000,
    loop:true,
    navText:['<i class="fas fa-chevron-left"></i>','<i class="fas fa-chevron-right"></i>'],
    nav:true,
    responsive:{
        0:{
            items:1,
        },
        600:{
            items:3,
        },
        1000:{
            items:5,
        },
        1200:{
          items:6,
        },
        1400:{
          items:7,
        }
    }
  });

// Product View Recently Added Product 

var owl_recent = $('#recent_product');

owl_recent.owlCarousel({
    margin:10,
    dots: false,
    autoplay: true,
    nav:true,
    autoplayTimeout: 5000,
    loop:true,
    navText:['<i class="fas fa-chevron-left"></i>','<i class="fas fa-chevron-right"></i>'],
    responsive:{
        0:{
            items:1,
            nav:true,
        },
        600:{
            items:3,
            nav:true,
        },
        1000:{
            items:5,
            nav:true,
        },
        1200:{
          items:6,
        },
        1400:{
          items:7,
        }
    }
  });

var owl_recent = $('.category_wise');

owl_recent.owlCarousel({
    margin:10,
    dots: false,
    autoplay: true,
    nav:true,
    autoplayTimeout: 5000,
    loop:true,
    navText:['<i class="fas fa-chevron-left"></i>','<i class="fas fa-chevron-right"></i>'],
    responsive:{
        0:{
            items:1,
            nav:true,
        },
        600:{
            items:3,
            nav:true,
        },
        1000:{
            items:5,
            nav:true,
        },
        1200:{
          items:6,
        },
        1400:{
          items:7,
        }
    }
  });


// Image Selection to view
  $('img').click(function(){
    if($(this).attr('id') == 'img1'){
      var value = $(this).attr('src');
      $('#photo_view').attr('src', value) 
    }
  });

  // Cart Logic
  if(localStorage.getItem('cart') == null)
  {
    var cart={};
  }
  else{    
    cart = JSON.parse(localStorage.getItem('cart'));
  }

  $('.cart').click(function(){
    
    var idstr= this.id.toString();
    if(cart[idstr] == undefined){
      var pro_photo = $('#pro_photo').val();
      var pro_name = $('#pro_name').text();
      var pro_stock = $('#pro_stock').val();
      var price = $('#price').text();
      var qty = 1
      cart[idstr] = {'product_photo': pro_photo, 'product_name': pro_name, 'product_stock': pro_stock, 'product_price': price, 'qty': qty};
    }
    
    $('span.badge').text(Object.keys(cart).length);
    localStorage.setItem('cart', JSON.stringify(cart));    
  });

  // Cart Badge Counter 
  if (Object.keys(cart).length == 0){
    $('span.badge').text();
  }
  else{
    $('span.badge').text(Object.keys(cart).length);
  }

  // Side Menu Sub-Category View
  $('.fa-span').click(function(){
    $(this).parent().next().slideToggle();
    console.log($(this).children().toggleClass('fa-toggle'))
  });

  $('.show_profile').click(function(){
    $('#pro_info').slideToggle(300);
  });

  $('.show_passwd').click(function(){
    $('#pro_passwd').slideToggle(300);
  });

});
