#!/home/okami/projects/icndb/.env/bin/python3
# -*- coding: utf-8 -*-
import re
import sys

from py_translator.__init__.py import __init__

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(__init__.py())
