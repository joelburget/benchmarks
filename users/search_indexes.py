from haystack import indexes, site
from benchmarks.users.models import UserProfile

class UserIndex(indexes.RealTimeSearchIndex):
  text = indexes.CharField(document=True, use_template=True)

site.register(UserProfile, UserIndex)
