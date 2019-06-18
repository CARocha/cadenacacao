// Template for custom "info" button
$.fancybox.defaults.btnTpl.info = '<button data-fancybox-info class="fancybox-button fancybox-button--info" title="Show caption">&#x25cf;&#x25cf;&#x25cf;</button>';

// Initialise fancybox with custom settings
$('[data-fancybox="images"]').fancybox({
  preventCaptionOverlap : false,
  infobar: false,

  // Disable idle
  idleTime : 0,

  // Display only these two buttons
  buttons : [
    'info', 'close'
  ],

  // Custom caption content
  caption : function( instance, obj ) {
    return '<div><p class="fancy-nav"><a data-fancybox-prev title="Previous" tabindex="1">&lsaquo;</a> <a data-fancybox-next title="Next" tabindex="2">&rsaquo;</a> &nbsp; <span data-fancybox-index></span> de <span data-fancybox-count></span> Productos</p>' + $(this).find('.caption').html() + '</div>';
  },

  onInit: function(instance) {

    // Toggle caption on tap
    instance.$refs.container.on('touchstart', '[data-fancybox-info]', function(e) {
      e.stopPropagation();
      e.preventDefault();

      instance.$refs.container.toggleClass('fancybox-vertical-caption');
    });

    // Display caption on button hover
    instance.$refs.container.on('mouseenter', '[data-fancybox-info]', function(e) {
      instance.$refs.container.addClass('fancybox-vertical-caption');

      // Hide caption when mouse leaves caption area
      instance.$refs.caption.one('mouseleave', function(e) {
        instance.$refs.container.removeClass('fancybox-vertical-caption');
      });

    });

  }

});