#!/usr/bin/env python

#
# Copyright (C) 2014 by Georgina Abou elkheir georgina20055@gmail.com 
# coauthor Skarvelis <sl45sms@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import re,tempfile, zipfile, os, sys, getopt,shutil

try:
 import xml.etree.cElementTree as ET
except ImportError:
 import xml.etree.ElementTree as ET
import PythonMagick as Magick


def setORAlayer(stack,src,name,x,y,visibility):
    layer = ET.Element('layer')
    stack.append(layer)
    layer = layer.attrib
    layer['src'] = src
    layer['name'] = name
    layer['x'] = x
    layer['y'] = y
    layer['opacity'] = '1.0'
    if visibility=='No':
      layer['visibility'] = 'hidden' 
    else:
      layer['visibility'] = 'visible'
    return stack







########################################################################
#command line parammeters

options, remainder = getopt.getopt(sys.argv[1:], 'o:v:h', ['output=', 
                                                           'verbose',
                                                           'help',
                                                           ])
ora_filename=""
verbose=False
for opt, arg in options:
    if opt in ('-o', '--output'):
       ora_filename = arg
    elif opt in ('-v', '--verbose'):
          verbose = True
    elif opt in ('-h','--help'):
         print """
Usage: psd2ora [option] infile.psd\n
Options:
-o, --output  : Optional,if not set output filename 
                is the same with psd with extension .ora
-v, --verbose : Optional,letting you see just what the program is doing.
-h, --help    : This Help
"""
         exit(0)

if len(remainder)==0:
   print "You have to provide psd file see --help"
   exit(1)

psd_filename=remainder[0]

if ora_filename=="":
   ora_filename=remainder[0].replace(".psd",".ora")
   if ora_filename.endswith(".ora")==False:
	   ora_filename+=".ora"


########################################################################









#main

#prepare xml

#prepare tmp folders
tmpfolder = tempfile.mkdtemp('_cmykpsd2ora')
datafolder = tmpfolder+'/data'
thumbnailfolder = tmpfolder+'/Thumbnails'
os.mkdir(datafolder)
os.mkdir(thumbnailfolder)



#####################################################################


fr=os.popen("convert /tmp/"+psd_filename+" -channel RGBA -alpha Set -colorspace rgb -verbose info "+datafolder+"/output.png").read()    

images=re.findall("output\.png\[(\d*)\].*[\+\-](\d*)[\+\-](\d*)\s", fr)    



wt=os.

## identify /tmp/tmpdPPuTQ_cmykpsd2ora/data/output-0.png 
#/tmp/tmpdPPuTQ_cmykpsd2ora/data/output-0.png PNG 5250x3450 5250x3450+0+0 8-bit DirectClass 7.735MB 0.010u 0:00.039
##


outputWidth=
outputHeight=

#build image attributes
image = ET.Element('image')
imageAttr = image.attrib
imageAttr['w'] = outputWidth
imageAttr['h'] = outputHeight
imageAttr['xres']= '300'
imageAttr['yres']= '300' #hardcoded maybe dynamic?


stack = ET.SubElement(image, 'stack')
for imagetemp in reversed(images):
    index,x,y = imagetemp
    stack=setORAlayer(stack,'data/output-'+str(index)+'.png','layer'+index,x,y,'Yes')


#write stack.xml
xml = ET.tostring(image, encoding='UTF-8')
#print xml
f = open(tmpfolder+'/stack.xml', 'w')
f.write(xml)
f.close()


thump=os.popen("convert -size 256x256 "+datafolder+"/output-0.png "+thumbnailfolder+"/thumbnail.png").read()    


#ok now the zip.....
ora = zipfile.ZipFile(ora_filename, 'w')
ora.writestr('mimetype', 'image/openraster',zipfile.ZIP_STORED)
ora.write(tmpfolder+"/stack.xml","stack.xml",zipfile.ZIP_DEFLATED)
ora.write(thumbnailfolder+"/thumbnail.png","Thumbnails/thumbnail.png",zipfile.ZIP_DEFLATED)

#For every img
for img in os.listdir(datafolder):
    ora.write(datafolder+"/"+img,"data/"+img,zipfile.ZIP_DEFLATED)

ora.close()

#and finaly delete tmpfolder

#shutil.rmtree(tmpfolder)
