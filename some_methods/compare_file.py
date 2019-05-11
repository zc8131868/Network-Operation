#!/usr/bin/env python

import difflib

def compare_file():
	f1_url = input("pls input the url of file1:")
	f2_url = input("pls input the url of file2:")
	while(True):
		try:
			with open(f1_url) as f1:
				f1_lines = f1.readlines()
			with open(f2_url) as f2:
				f2_lines = f2.readlines()
			break
		except Exception as e:
			print(e)
			f1_url = input("pls input the url of file1:")
			f2_url = input("pls input the url of file2:")

	ratio = difflib.SequenceMatcher(None,f1_lines,f2_lines).ratio()
	print(ratio)

	if ratio != 1.0:
		d = difflib.HtmlDiff()
		res = d.make_file(f1_lines, f2_lines)
		with open("diff.html", "w") as f:
			f.write(res)
	else:
		print("The contents of these two files are the same")




