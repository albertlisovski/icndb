#!/home/okami/projects/icndb/.env/bin/python3
# -*- coding: utf-8 -*-
import re
import sys

from py_translator.html_translator.py import html_translator

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(html_translator.py())
