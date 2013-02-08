#!/usr/bin/python3
'''zyklon's photo orginizer
This program will read exif data to look for dates a photo was taken
then crete directories and move photos into them
pretty sure this now depends on gexiv2-dev - get mikuro to test'''

import os
import shutil
from gi.repository import GExiv2

def getFileList(srcDIR):
	'''first we need to get a list of files'''
	
	fileList = []
	
	while True:
		recurse = input("recurse in source? Y/N ")
		if recurse.lower() == "y":
			recurse = True
			break
		elif recurse.lower() == "n":
			recurse = False
			break
	
	if recurse == True:
		for r,d,f in os.walk(srcDIR):
			for files in f:
				if files.endswith(".JPG") or files.endswith(".JPEG") or files.endswith(".jpg") or files.endswith(".jpeg"):
					fileList.append(os.path.join(r,files))
	
	else:
		for files in os.listdir(srcDIR):
			if files.endswith(".JPG") or files.endswith(".JPEG") or files.endswith(".jpg") or files.endswith(".jpeg"):
				fileList.append(os.path.join(srcDIR,files))
	
	return fileList

def main():	
	while True:				#check if src dir exists
		srcDIR = input("Source directory of unsorted photos: ")
		srcDIR = os.path.expanduser(srcDIR)
		if os.path.exists(srcDIR):
			break
		else: print ("invalid path")
	while True:				#check if output dir exists and create
		destDIR = input("Destination for sorted photos: ")
		destDIR = os.path.expanduser(destDIR)
		if os.path.exists(destDIR):
			print ("path exists")
			break
		else:
			createDIR = input("Create output DIR? ")
			if createDIR.lower() == "y":
				os.makedirs(destDIR)
				break
	copymove = input("Would you like to copy or move the files? C/M ")
	
	for image in getFileList(srcDIR):									#Here's the magic bit
		try:
			dateTaken = GExiv2.Metadata(image).get_date_time()
			yearDIR = os.path.join(destDIR, str(dateTaken.year))
			moDIR = os.path.join(yearDIR, str(dateTaken.year) + "_" + str(dateTaken.month))
			dayDIR = os.path.join(moDIR, str(dateTaken.year) + "_" + str(dateTaken.month) + "_" + str(dateTaken.day))
			exif = True
		except:
			exif = False
																		
		if exif == True:
			if not os.path.exists(dayDIR):
				os.makedirs(dayDIR)
		
			if copymove.lower() == "m":
				shutil.move(image, dayDIR)
				print ("Moved", image, "to", dayDIR)
			else:
				shutil.copy(image, dayDIR)
				print ("Copied", image, "to", dayDIR)
		else:
			print ("No EXIF data for", image)

		
		
		
		


main()
