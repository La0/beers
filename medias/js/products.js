$(function(){
  
  $('#products_content p.product').click(function(){
    product_id = $(this).attr('id').substr(8);
    
    //Select product
    $('form#price_form input[name=product]').val(product_id);
    
  });
  
});