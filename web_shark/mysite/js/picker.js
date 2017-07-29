
    $(document).ready(function () {
     $("#selectImage").imagepicker({
         hide_select: true,
         show_label: true
     });

    //  var $container = $('.image_picker_selector');
    //  // initialize
    //  $container.imagesLoaded(function () {
    //      $container.masonry({
    //          columnWidth: 30,
    //          itemSelector: '.thumbnail'
    //      });
    //  });

 });

 function getSelectedIndexes (oListbox)
 {
   var arrIndexes = new Array;
   for (var i=0; i < oListbox.options.length; i++)
   {
       if (oListbox.options[i].selected) arrIndexes.push(i);
   }
   return arrIndexes;
 };
