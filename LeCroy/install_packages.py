# -*- coding: utf-8 -*-
"""
Created on Feb  15  2024

script to install needed packages for LeCroy oscilloscope

@author: Alex Kedziora
"""

import sys
import subprocess

# implement pip as a subprocess:
#subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'lecroydso'])