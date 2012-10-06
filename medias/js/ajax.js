$(function(){
  /* Load via Ajax a sub page */
  $('a.ajax-load').click(function(){
    var target = $('#' + $(this).attr('target') );
    var href = $(this).attr('href');
    var btn = $(this);
    
    $.ajax({
      type  : 'GET',
      url   : href,
      success : function(data){
        btn.hide();
        target.html(data).addClass('ajax-loaded');
      },
      error : function(err){
        console.log('Failed to load '+href+' : '+err);
      }
    });
    
    return false;
  });
  
  /* Load via ajax a form */
  $('.ajax-loaded form').live('submit', function(){
    var href = $(this).attr('action');
    var target = $(this).parent('.ajax-loaded');

    // Rebuild form data
    var data = {};
    $(this).find(':input').each(function(index, elt){
      data[$(elt).attr('name')] = $(elt).val();
    });

    $.ajax({
      type  : 'POST',
      url   : href,
      data  : data,
      success : function(data){
        target.html(data).addClass('ajax-loaded');
      },
      error : function(err){
        console.log('Failed to load '+href+' : '+err);
      }
    })
    
    return false;
  });
});