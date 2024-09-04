/* Project specific Javascript goes here. */
$(document).ready(function(){
    // Activar el popover cuando se hace clic en '.popover-cell'
    $('.popover-cell').click(function(){
        $(this).popover('toggle');
    });

    // Cerrar el popover activo cuando se hace clic fuera de él
    $(document).on('click', function (e) {
        if ($(e.target).data('toggle') !== 'popover' && $(e.target).parents('.popover').length === 0) {
            $('.popover-cell').popover('hide');
        }
    });
});

$(function () {
    $('select[name="level1"]').on('change', function () {
        var id = $(this).val();
        var select_level2 = $(this).closest('form').find('select[name="level2"]');
        var select_level3 = $(this).closest('form').find('select[name="level3"]');
        var options = '<option value="">---------</option>';
        select_level3.html(options);
        if(id === ''){
            select_level2.html(options);
            return false;
        }
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'load_level2',
                'id': id
            },
            dataType: 'json',
        }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
                $.each(data, function (key, value) {
                    options+='<option value="'+value.id+'">'+value.name+'</option>';
                });
                return false;
            }
            message_error(data.error);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {
            select_level2.html(options);
        });
    });

    $('select[name="level2"]').on('change', function () {
        var id = $(this).val();
        var select_level3 = $(this).closest('form').find('select[name="level3"]');
        var options = '<option value="">---------</option>';

        if(id === ''){
            select_level3.html(options);
            return false;
        }

        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'load_level3',
                'id': id
            },
            dataType: 'json',
        }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
                $.each(data, function (key, value) {
                    options+='<option value="'+value.id+'">'+value.name+'</option>';
                });
                return false;
            }
            message_error(data.error);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {
            select_level3.html(options);
        });
    });
});

$.fn.extend({
    treed: function (o) {

      var openedClass = 'glyphicon-minus-sign';
      var closedClass = 'glyphicon-plus-sign';

      if (typeof o != 'undefined'){
        if (typeof o.openedClass != 'undefined'){
        openedClass = o.openedClass;
        }
        if (typeof o.closedClass != 'undefined'){
        closedClass = o.closedClass;
        }
      };

        //initialize each of the top levels
        var tree = $(this);
        tree.addClass("tree");
        tree.find('li').has("ul").each(function () {
            var branch = $(this); //li with children ul
            //branch.prepend("<i class='indicator glyphicon " + closedClass + "'></i>");
            branch.addClass('branch');
            branch.on('click', function (e) {
                if (this == e.target) {
                    //var icon = $(this).children('i:first');
                    //icon.toggleClass(openedClass + " " + closedClass);
                    $(this).children().children().toggle();
                }
            })
            //branch.children().children().toggle();
        });

        /*
        //fire event from the dynamically added icon
      tree.find('.branch .indicator').each(function(){
        $(this).on('click', function () {
            $(this).closest('li').click();
        });
      });
        //fire event to open branch if the li contains an anchor instead of text
        tree.find('.branch>a').each(function () {
            $(this).on('click', function (e) {
                $(this).closest('li').click();
                e.preventDefault();
            });
        });
        //fire event to open branch if the li contains a button instead of text
        tree.find('.branch>button').each(function () {
            $(this).on('click', function (e) {
                $(this).closest('li').click();
                e.preventDefault();
            });
        });*/
    }
});

//Initialization of treeviews

$('#tree3').treed({openedClass:'glyphicon-chevron-right', closedClass:'glyphicon-chevron-down'});

$(function () {
    $('#message_modal').modal('show');
});


// drag and drop
function readURL(input, cronograma_id) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            //$('.image-upload-wrap').hide();
            var fileUploadContent = $('#file-upload-content-'+cronograma_id);
            var fileUploadImage = $('#file-upload-image-'+cronograma_id);
            var fileUploadImageSaved = $('#file-upload-image-saved-'+cronograma_id);

            fileUploadContent.show();
            fileUploadImage.attr('src', e.target.result);
            fileUploadImageSaved.hide();
            //$('.image-title').html(input.files[0].name);
        };
        reader.readAsDataURL(input.files[0]);
    } else {
        removeUpload(cronograma_id);
    }
}

function removeUpload(cronograma_id) {
    var imageUploadWrap = $('.image-upload-wrap');
    var fileUploadInput = $('.file-upload-input');
    var fileUploadContent = $('#file-upload-content-'+cronograma_id);
    fileUploadInput.replaceWith(fileUploadInput.clone());
    fileUploadContent.hide();
    imageUploadWrap.show();
}

$('.image-upload-wrap').bind('dragover', function () {
    $('.image-upload-wrap').addClass('image-dropping');
});
$('.image-upload-wrap').bind('dragleave', function () {
    $('.image-upload-wrap').removeClass('image-dropping');
});


// progress metas
$(function() {
   var Accordion = function(el, multiple) {
      this.el = el || {};
      this.multiple = multiple || false;

      var links = this.el.find('.link');

      links.on('click', {el: this.el, multiple: this.multiple}, this.dropdown)
   }

   Accordion.prototype.dropdown = function(e) {
      var $el = e.data.el;
         $this = $(this),
         $next = $this.next();

      $next.slideToggle();
      $this.parent().toggleClass('open');

      if (!e.data.multiple) {
         $el.find('.submenu').not($next).slideUp().parent().removeClass('open');
      };
   }

   var accordion = new Accordion($('#accordion'), false);
});


var accordion = (function(){
  var $accordion = $('.js-accordion');
  var $accordion_header = $accordion.find('.js-accordion-header');
  var $accordion_item = $('.js-accordion-item');

  // default settings
  var settings = {
    // animation speed
    speed: 400,

    // close all other accordion items if true
    oneOpen: false
  };

  return {
    // pass configurable object literal
    init: function($settings) {
      $accordion_header.on('click', function() {
        accordion.toggle($(this));
      });

      $.extend(settings, $settings);

      // ensure only one accordion is active if oneOpen is true
      if(settings.oneOpen && $('.js-accordion-item.active').length > 1) {
        $('.js-accordion-item.active:not(:first)').removeClass('active');
      }

      // reveal the active accordion bodies
      $('.js-accordion-item.active').find('> .js-accordion-body').show();
    },
    toggle: function($this) {

      if(settings.oneOpen && $this[0] != $this.closest('.js-accordion').find('> .js-accordion-item.active > .js-accordion-header')[0]) {
        $this.closest('.js-accordion')
               .find('> .js-accordion-item')
               .removeClass('active')
               .find('.js-accordion-body')
               .slideUp()
      }

      // show/hide the clicked accordion item
      $this.closest('.js-accordion-item').toggleClass('active');
      $this.next().stop().slideToggle(settings.speed);
    }
  }
})();

$(document).ready(function(){
  accordion.init({ speed: 300, oneOpen: true });
});

