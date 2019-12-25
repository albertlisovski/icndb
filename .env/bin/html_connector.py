#!/home/okami/projects/icndb/.env/bin/python3
# -*- coding: utf-8 -*-
import re
import sys

from py_translator.html_connector.py import html_connector

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(html_connector.py())
