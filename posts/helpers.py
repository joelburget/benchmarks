import os
import zipfile
import commands
from benchmarks.settings import MEDIA_ROOT

INVALID_FILES = (
  r'^**$',
  r'^**$',
)

def validate_file(file):
  return True


