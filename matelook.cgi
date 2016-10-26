#!/usr/bin/python

import cgi
from wsgiref.handlers import CGIHandler
from matelook import app

CGIHandler().run(app)