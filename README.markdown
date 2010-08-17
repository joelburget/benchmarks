OSU RSRG Benchmarks Website
===========================

This is the README for the OSU RSRG Benchmarks website.  See the TODO file for work-in-progress information.

CSS Workflow
------------

CSS development is done using [LessCSS](http://lesscss.org/index.html).  See the homepage for installation (requires ruby/rubygems).  To use less, code your CSS in a .less file, and compile it to css with lessc:

    $ vim benchmarks.less

    ...

    $ lessc benchmarks.less
    $ ls
    benchmarks.css benchmarks.less

Credits
-------

The [Fugue](http://p.yusukekamiyamane.com) iconset was used in this project.
