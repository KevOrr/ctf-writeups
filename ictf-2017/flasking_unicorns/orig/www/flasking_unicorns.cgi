#!/usr/bin/env python
from wsgiref.handlers import CGIHandler

import sys
sys.path.append('../ro')

import flasking_unicorns
import os

CGIHandler.os_environ = os.environ 
CGIHandler().run(flasking_unicorns.app)

