/*
 * textEditor, jQuery plugin
 * Copyright (c) 2010 Colin Drake
 * Licensed under the MIT license.
*/

(function ($) {
  $.fn.extend({
    textEditor: function (options) {
      /*
       * textEditor options
       *
       * buttons - Lists of lists of 3 elements, containing tooltips, formatting
       *  text, and an icon
       * icons_dir - Directory to look for icons in
       * substitution_string - String contained inside button to replace with
       *  real text
       * prompt_string - String to display for 
       * class_prefix - Prefix classname to be used
       *  class_prefix + 'container' - class used for container div
       *  class_prefix + 'separator' - class used for separator images
       *  class_prefix + 'button' - class used for button images
      */
      var defaults = {
        buttons: [],
        separator_icon: 'foo.png',
        icons_dir: '',
        substitution_string: '%s',
        prompt_string: 'type text here',
        class_prefix: 'texteditor-',
      };
      var options = $.extend(defaults, options);

      return this.each(function () {
        /* Add container div */
        var obj = this;
        var div = $(document.createElement('div'))
                            .addClass(options.class_prefix + 'container')
                            .insertBefore(this);

        /* Add buttons */
        for (var i = 0; i < options.buttons.length; ++i) {
          var button = options.buttons[i];

          if (button.length == 0) {
            /* Separator */
            $(document.createElement('img'))
                      .attr({
                        'src': options.icons_dir + options.separator_icon,
                      })
                      .addClass(options.class_prefix + 'separator')
                      .appendTo(div);
          } else {
            /* Formatting button */
            var tooltip = button[0],
                text = button[1],
                icon = button[2];

            $(document.createElement('img'))
                      .attr({
                        'src': options.icons_dir + icon,
                        'title': tooltip,
                        'style': 'cursor:pointer;',
                        'alt': text})
                      .addClass(options.class_prefix + 'button')
                      .click(function() {
                        /* Get selection */
                        var sel = $(obj).getSelection(),
                            txt = $(this).attr('alt');
                        
                        /* Replace or insert text */
                        if (sel.text != '') {
                          var repl = txt.replace(options.substitution_string, 
                                                 sel.text);
                          $(obj).replaceSelection(repl, true);
                        } else {
                          var repl = txt.replace(options.substitution_string,
                                                 options.prompt_string),
                              start = repl.indexOf(options.prompt_string),
                              len = options.prompt_string.length;
                          $(obj).insertAtCaretPos(repl);
                          $(obj).setSelection(sel.start + start,
                                              sel.start + start + len);
                        }

                        return false;
                      })
                      .appendTo(div);
          }
        }
      });
    }
  });
})(jQuery);
