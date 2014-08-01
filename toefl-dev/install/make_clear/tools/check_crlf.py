#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

def traverse(path):
    for f in os.listdir(path):
        if (f == '.git'):
            continue
        p = os.path.join(path, f)
        ext = os.path.splitext(p)[1]
        if (os.path.isdir(p)):
            traverse(p)
        elif (ext in ['.py', '.cpp', '.h', '.gitignore', '.cctpl', '.txt', '.md', '.sh']):
            try:
                with open(p, "rb") as f:
                    cnt = f.read()
                if (cnt.find('\r\n') >= 0):
                    print('Convert %s ...' % p)
                    with open(p, "wb") as f:
                        f.write(cnt.replace('\r\n', '\n'))
            except Exception:
                logging.exception('Check %s failed.' % p)

traverse('.')
