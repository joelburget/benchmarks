from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.models import Group
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage

def index(request):
  # Search, or index
  if 'searchtxt' in request.GET:
    searchtxt = request.GET['searchtxt']
    pgroups = Group.objects.filter(name__icontains=searchtxt)
  else:
    searchtxt = ''
    pgroups = Group.objects.all()

  # Paginate
  paginator = Paginator(pgroups, 10)
  
  try:
    page = int(request.GET.get('page', '1'))
  except ValueError:
    page = 1

  try:
    groups = paginator.page(page)
  except (EmptyPage, InvalidPage):
    groups = paginator.page(paginator.num_pages)

  return render_to_response('groups/index.html', { 'searchtxt' : searchtxt, 'groups' : groups }, context_instance=RequestContext(request))

def detail(request, group_id):
  group = get_object_or_404(Group, pk=group_id)
  return render_to_response('groups/detail.html', { 'group' : group }, context_instance=RequestContext(request))

def join(request):
  if request.method == 'POST' and request.user.is_authenticated():
    # Join this group, if authenticated
    groupid = request.POST['groupid']
    group = Group.objects.get(pk=groupid)
    request.user.get_profile().group = group
    request.user.get_profile().save()
    return HttpResponseRedirect('/groups/' + groupid)
  else:
    # Bad request
    return HttpResponseRedirect('/')

def leave(request):
  if request.method == 'POST' and request.user.is_authenticated():
    # Leave this group, if authenticated
    groupid = request.POST['groupid']
    group = Group.objects.get(pk=groupid)
    request.user.get_profile().group = None
    request.user.get_profile().save()
    return HttpResponseRedirect('/groups/' + groupid)
  else:
    # Bad request
    return HttpResponseRedirect('/')
