"""
Deployment script for benchmarks project

Usage:

    fab -l          Get a list of commands, and this help
    fab [commands]  Execute given commands

Legend:

    (E)   Environment commands - set server to deploy to
    (R)   Remote commands - run on machines set by (E) commands
    (L)   Local commands - run on this local machine
"""

#
# Imports
#

from __future__ import with_statement
import os
from fabric.api import *

#
# Global configuration
#

env.git_github = "git@github.com:joelburget/benchmarks.git"
env.git_from = "origin"
env.git_to = "master"

env.apps_to_test = "extended_comments groups posts users"
env.local_path = os.path.abspath(os.curdir)

#
# Per-environment configuration
#

def production():
  """Load configuration for CSE server environment (E)"""
  env.hosts = ["syrus.cse.ohio-state.edu"]
  env.user = "benchmarkweb"
  env.path = "~/benchmarks"

#
# Tasks
#

# Local

def test():
  """Runs tests locally with the django test framework (L)"""
  require("apps_to_test")
  local("python manage.py test %s" % env.apps_to_test)

def css():
  """Compiles CSS locally with lessc (L)"""
  with cd("assets/css"):
    local("lessc benchmarks.less")

# Remote

def syncdb():
  """Syncs remote database destructively (R)"""
  require("path", provided_by=[production])
  with cd(env.path):
    run("python manage.py syncdb --noinput")

def pull():
  """Pulls latest commit from github to remote server (R)"""
  require("path", provided_by=[production])
  with cd(env.path):
    run("git pull") # %s %s %s" % (env.git_github, env.git_from, env.git_to))

def deploy():
  """Deploys to a remote server (unsafe) (R)"""
  require("path", provided_by=[production])
  css()
  pull()
  syncdb()

  with cd(env.path):
    put(os.path.join(env.local_path, "assets/css/benchmarks.css"), 
        os.path.join(env.path, "assets/css/"))

def deploy_safe():
  """Deploys to a remote server, only if tests pass (R)"""
  test()
  deploy()
