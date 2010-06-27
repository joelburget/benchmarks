OSU RSRG Benchmarks Website
===========================

This is the README for the OSU RSRG Benchmarks website.  See the TODO file for work-in-progress information.

Basic Database Workflow
-----------------------

Note: This application does not use Django itself for database/model development.  A database migration library, South, is used (see http://south.aeracode.org/ for details).  To use this, code your model as usual, but use South to migrate from one version of the model to the next, instead of syncdb and manually altering tables.

Here is an example work session, updating the database model for a Post:

    $ vim posts/model.py

    ... Proceed to make changes to the Model, in this example, adding a foobar field...
    
    $ python manage.py schemamigration posts --auto
    
    ...
    Created 0009_add_field_foobar.py. You can now apply this migration with ./manage.py migrate posts

    $ python manage.py migrate posts
    
    ...
    
    $ git add posts/migrations/0009_add_field_foobar.py
    $ git commit -a -m "Added foobar field to Post model."

After following these steps, the model will be changed, the database migrations will be created, the database itself will be updated, and git will be aware of your changes.  Please note that adding the migration file to git is easy to forget, but very important.

Follow this example for each change you make to the database, whether it is an addition or removal of a field.  Please see the South tutorial/documentation for more information.
