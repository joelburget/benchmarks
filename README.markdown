OSU RSRG Benchmarks Website
===========================

This is the README for the OSU RSRG Benchmarks website.  See the TODO file for work-in-progress information.

Deployment
----------

- Change the SECRET_KEY
- ...

Edit and place the following in email_settings.py to allow user registrations:

    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'USERNAME@gmail.com'
    EMAIL_HOST_PASSWORD = 'PASSWORD'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    ADMIN_EMAIL = 'USERNAME@DOMAIN.com'

Note: Emails for manual confirmation of user accounts will be sent to ADMIN_EMAIL.

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
