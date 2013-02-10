#!/usr/bin/python3
'''Zyklon's image sorterrhhr'''

import getopt
import sys
import os
import shutil
from gi.repository import GExiv2

def usage():
	print ("""A photo sorting utility, sorts photos into a new directory by date
	
	Usage: exifPictures [-hrmio]"
	
	-h,	--help			Print this message and exit
	-r,	--recursive		Recursive searching on input directory
	-m,	--move			Move files instead of copy to output directory
	-i,	--input			Input directory
	-o,	--output		Output directory""")
	
def getFileList(srcDIR, recurse):
	'''returns the list of files for processing'''

	fileList = []

	if recurse == True:
		for r,d,f in os.walk(srcDIR):
			for files in f:
				if files.endswith(".JPG") or files.endswith(".JPEG") or files.endswith(".jpg") or files.endswith(".jpeg"):	#regex goes here
					fileList.append(os.path.join(r,files))
	
	else:
		for files in os.listdir(srcDIR):
			if files.endswith(".JPG") or files.endswith(".JPEG") or files.endswith(".jpg") or files.endswith(".jpeg"):
				fileList.append(os.path.join(srcDIR,files))
	
	return fileList

def workerFunction(fileList, destDIR, moveFiles):
	for image in fileList:									
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
		
			if moveFiles == True:
				shutil.move(image, dayDIR)
				print ("Moved", image, "to", dayDIR)
			else:
				shutil.copy(image, dayDIR)
				print ("Copied", image, "to", dayDIR)
		else:
			print ("No EXIF data for", image)


def main():
	
	srcDIR = 'none'														#set initial values for options
	destDIR = 'none'
	recurse = False
	moveFiles = False

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hrmi:o:", ["help", "recursive", "move", "input=", "output="])
	except getopt.GetoptError as err:
		usage()
		print(err)
		sys.exit(2)
	
	for o, a in opts:													#check arguments and change initial values
		if o in ("-h", "--help"):
			usage()
			sys.exit()
			
		elif o in ("-r", "--recursive"):
			recurse = True
			 
		elif o in ("-m", "--move"):
			moveFiles = True
		
		elif o in ("-i", "--input="):
			srcDIR = os.path.expanduser(a)
			if not os.path.exists(srcDIR):
				print ("Input directory does not exist")
				sys.exit(2)
			
		elif o in ("-o", "--output="):
			destDIR = os.path.expanduser(a)
			if not os.path.exists(destDIR):
				os.makedirs(destDIR)
				print ("Created Output directory")

																		
	fileList = getFileList(srcDIR, recurse)
	workerFunction(fileList, destDIR, moveFiles)
	

main()
