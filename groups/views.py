from benchmarks.helpers import *
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.models import Group
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

def index(request):
  # Search, or index
  if 'searchtxt' in request.GET:
    searchtxt = request.GET['searchtxt']
    pgroups = Group.objects.filter(name__icontains=searchtxt)
  else:
    searchtxt = ''
    pgroups = Group.objects.all()

  groups = get_page_of_objects(pgroups, request) 
  return render_to_response('groups/index.html', { 'searchtxt' : searchtxt, 'groups' : groups }, context_instance=RequestContext(request))

def detail(request, group_id):
  group = get_object_or_404(Group, pk=group_id)
  return render_to_response('groups/detail.html', { 'group' : group }, context_instance=RequestContext(request))

@require_POST
@login_required
def join(request):
  # Join this group
  groupid = request.POST['groupid']
  group = Group.objects.get(pk=groupid)
  request.user.get_profile().group = group
  request.user.get_profile().save()
  return HttpResponseRedirect('/groups/' + groupid)

@require_POST
@login_required
def leave(request):
  # Leave this group
  groupid = request.POST['groupid']
  group = Group.objects.get(pk=groupid)
  request.user.get_profile().group = None
  request.user.get_profile().save()
  return HttpResponseRedirect('/groups/' + groupid)
