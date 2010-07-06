# Migration script to create profiles for all users that don't have them.
#
# Run mange.py shell (NOT python.exe)
# >> from scripts import user_profiles
# >> user_profile.run()
from django.contrib.auth.models import User
from benchmarks.users.models import UserProfile

def run():
  for person in User.objects.all():
    try:
      profile = person.get_profile()

      print 'Skipping %s, because a profile is already associated with this user.' % (person.username,)
    except:
      profile = UserProfile(user=person, bio='')
      profile.save()

      print 'Profile created for %s.' % (person.username,)
