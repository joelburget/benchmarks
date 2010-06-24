#This is stolen from http://github.com/nshah/django-comment-sanitize/blob/master/__init__.py
import sys
import os
#import logging
#LOG_FILENAME = '/Users/joelburget/benchmarks/log'
#logging.basicConfig(filename = LOG_FILENAME, level = logging.DEBUG)

from django.db.models import signals
from django.dispatch import dispatcher
from django.contrib.comments.models import Comment

import html5lib
from html5lib import sanitizer

sys.path.append(os.path.realpath(__file__) + 'html5lib/')

def sanitize_comment(sender, instance, **kwargs):
    #logging.debug(instance.comment)
    p = html5lib.HTMLParser(tokenizer=sanitizer.HTMLSanitizer)
    # childNodes[0] -> html, childNodes[1] -> body, the 6:-7 drops the open/close body tags
    instance.comment = p.parse(instance.comment).childNodes[0].childNodes[1].toxml()[6:-7]
    #logging.debug(instance.comment)

signals.pre_save.connect(sanitize_comment, sender=Comment)
