#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from PIL import Image

if (len(sys.argv) < 2):
    print('pic2bmp.py input-file [output-file]')
    sys.exit(0)

input_path = sys.argv[1]
if (len(sys.argv) < 3):
    output_path = os.path.splitext(input_path)[0] + '.bmp'
    if (os.path.isfile(output_path)):
        print('Default output file "%s" exists. Please specify your output '
              'file.' % output_path)
        sys.exit(0)
else:
    output_path = sys.argv[2]
im = Image.open(input_path)
im.save(output_path)
