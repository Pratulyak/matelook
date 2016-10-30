#!/usr/bin/env python3.5

import cgi
from wsgiref.handlers import CGIHandler
from matelook import app


CGIHandler().run(app)