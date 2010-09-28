jquery.textEditor
=================

Lightweight jQuery plugin that adds buttons to format plain text in a text input.

->![Screen cap](http://github.com/cfdrake/jquery-textEditor/raw/master/demo/images/screenie.png "Screenshot")<-

Usage
-----

See `demo/` folder, or...

    <!-- Include jquery, atools, and texteditor scripts in the <head> -->
    <script type="text/javascript" src="path/to/js/jquery.a-tools-1.5.2.min.js"></script>
    <script type="text/javascript" src="path/to/js/jquery.plaintxtformat.js"></script>

    <!-- ... -->

    <!-- In document.ready -->
    $('#my-textarea').textEditor({
      controls: {
        bold: '[b]%s[/b]',
        italic: '[i]%s[/i]',
        // ...
      }
    });

...will add buttons for bold and italic typefaces above the textarea. Clicking on a button with a text selection will surround it with the selected formatting. Without a text selection, the formatting will be added at the current cursor position, with the substitution string (default "%s") replaced with a filler text.

License
-------

Copyright (c) 2010 Colin Drake

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in
 all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 THE SOFTWARE.
