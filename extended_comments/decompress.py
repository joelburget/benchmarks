import os
import tarfile
import zipfile

from benchmarks.extended_comments.models import ExtendedCommentFile

def decompress(filepath, comment):
  # Get output path
  print filepath
  outputpath = os.path.split(filepath)[0]

  if zipfile.is_zipfile(filepath):
    # Zipfiles
    z = zipfile.ZipFile(filepath, 'r')
    z.extractall(path=outputpath)
    files = z.namelist()
  elif tarfile.is_tarfile(filepath):
    # Tarballs
    t = tarfile.open(filepath)
    t.extractall(path=outputpath)
    files = t.getnames()
    t.close()
  else:
    # None, file list is empty, so we don't add to model
    files = []

  # Add all files to the comment
  for name in files:
    unzippedfile = os.path.join(outputpath, name)
    modelfile = 'uploads/comments/%s/%s' % (comment.pk, name,) 

    # Note, don't add directories, otherwise Django can't remove them without
    # complaining with error messages.
    if not os.path.isdir(unzippedfile):
      filemod = ExtendedCommentFile(file=modelfile, parent=comment)
      #filemod = ExtendedCommentFile()
      #filemod.parent = comment
      filemod.save()
