from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response
from django.contrib.auth.models import Group
from django.template import RequestContext
from django.http import HttpResponseRedirect

def index(request):
  groups = get_list_or_404(Group)
  return render_to_response('groups/index.html', { 'groups' : groups }, context_instance=RequestContext(request))

def detail(request, group_id):
  group = get_object_or_404(Group, pk=group_id)
  return render_to_response('groups/detail.html', { 'group' : group }, context_instance=RequestContext(request))

def join(request):
  if request.method == 'POST' and request.user.is_authenticated():
    # Join this group, if authenticated
    groupid = request.POST['groupid']
    group = Group.objects.get(pk=groupid)
    request.user.groups.add(group)
    request.user.save()
    return HttpResponseRedirect('/groups/' + groupid)
  else:
    # Bad request
    return HttpResponseRedirect('/')

def leave(request):
  if request.method == 'POST' and request.user.is_authenticated():
    # Leave this group, if authenticated
    groupid = request.POST['groupid']
    group = Group.objects.get(pk=groupid)
    request.user.groups.remove(group)
    request.user.save()
    return HttpResponseRedirect('/groups/' + groupid)
  else:
    # Bad request
    return HttpResponseRedirect('/')
