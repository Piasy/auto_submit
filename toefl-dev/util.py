"""Utility functions for processing images for delivery to Tesseract"""

import os
import re
import ImageEnhance, Image

import errors, subprocess

def image_to_scratch(im, scratch_image_name):
	"""Saves image in memory to scratch file.  .bmp format will be read correctly by Tesseract"""
	im.save(scratch_image_name, dpi=(200,200))
	make_clear()

def make_clear():
        args = ['./make_clear']
        proc = subprocess.Popen(args)
        retcode = proc.wait()
        if retcode!=0:
                errors.check_for_errors()

def	retrieve_text(scratch_text_name_root):
	inf = file(scratch_text_name_root + '.txt')
	text = inf.read()
	inf.close()
	ret = ''
	for i in range(0, len(text)):
		if re.search('[a-zA-Z0-9]', text[i]) != None:
			ret += text[i]
	return ret.lower()

def perform_cleanup(scratch_image_name, scratch_text_name_root):
	"""Clean up temporary files from disk"""
	for name in (scratch_image_name, scratch_text_name_root + '.txt', "tesseract.log"):
		try:
			os.remove(name)
		except OSError:
			pass

def log(msg):
	fl = open('log.txt', 'a')
	fl.write(msg + "\n")
	fl.close()

if __name__=='__main__':
	#print retrieve_text('temp')
	im = Image.open('1.jpg')
	bb = ImageEnhance.Brightness(im)
	cc = ImageEnhance.Contrast
