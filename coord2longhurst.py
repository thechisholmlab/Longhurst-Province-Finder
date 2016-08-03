#!/usr/bin/python

'''
COORDS2LONGHURST

This script takes as input latitude and longitude coordinates and returns the 
Longhurst Province where the coordinate is found.  It works by parsing a file that 
contains lat/long coordinates that bound each province and performing the Crossings Test
on each province.  The Crossings Test is used in computer graphics to quickly 
determine if a point is within or outside a polygon by "drawing" a line east from the
input coordinate and seeing how many crossings the line makes with the polygon border. 
If there is an odd number of crossings, the point is within the polygon, otherwise the
point is outside the polygon.


dependent on:
	longhurst.xml:	A .gml file that contains the coordinates that bound each province
	
in:
	myLat:	Northerly latitude ranging from -90 to 90
	myLon:  Easterly longitude ranging from -180 to 180
	
out:
	Longhurst province code and name where the coordinate can be found. 
	If the coordinate is on land, or otherwise unassociated with a province, 
		a list of candidate provinces to check manually will be returned.
		
@ Sara Collins.  MIT.  3/18/2015

'''

import sys
from xml.dom.minidom import *


### Get lat and lon from command line argument list
###--------------------------------------------------------------------------

ppFileName = string(sys.argv[1])
imgFileName = string(sys.argv[2])	
	
	
### Parse GML data from longhurst.xml
###--------------------------------------------------------------------------

provinces = {}
tree = parse('longhurst.xml')

for node in tree.getElementsByTagName('MarineRegions:longhurst'):

	# 1. Get province code, name and bounding box from file
	provCode = node.getElementsByTagName('MarineRegions:provcode')[0].firstChild.data
	provName = node.getElementsByTagName('MarineRegions:provdescr')[0].firstChild.data
	fid = node.getAttribute("fid")
	b = node.getElementsByTagName('gml:coordinates')[0].firstChild.data

	# 2. Parse bounding box coordinates
	b = b.split(' ')
	x1,y1 = b[0].split(',')
	x2,y2 = b[1].split(',')
	x1 = float(x1)
	y1 = float(y1)
	x2 = float(x2)
	y2 = float(y2)

	provinces[fid] = {'provName': provName, 'provCode': provCode, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}


### Find which candidate provinces our coordinates come from.
###--------------------------------------------------------------------------

inProvince = {}
for p in provinces:
	inLat = 0
	inLon = 0
	
	if (myLat>=provinces[p]['y1'] and myLat<=provinces[p]['y2']):
		inLat = 1
		
	if (myLon>=provinces[p]['x1'] and myLon<=provinces[p]['x2']):
		inLon = 1
	
	if inLat and inLon:
		inProvince[p] = True	
		
		
### Perform Crossings Test on each candidate province.
###--------------------------------------------------------------------------

for node in tree.getElementsByTagName('MarineRegions:longhurst'):
	fid = node.getAttribute("fid")
	
	if inProvince.get(fid):
		crossings = 0
		
		## 1. Get all coordinate pairs for this province.
		geom = node.getElementsByTagName('MarineRegions:the_geom')
		
		for g in geom:
			c = g.getElementsByTagName('gml:coordinates')
			
			for i in c:
				ii = i.childNodes
				coordStr = ii[0].data		#<--- contains coordinate strings
				P = coordStr.split(' ')
				
				pairs = []
				for p in P:
					[lon,lat] = p.split(',')
					pairs.append([float(lon),float(lat)])	
					
				## 2. Use pair p and p+1 to perform Crossings Test.
				for i in range(len(pairs)-1):
					# test latitude
					passLat = (pairs[i][1]>=myLat and pairs[i+1][1]<=myLat) or (pairs[i][1]<=myLat and pairs[i+1][1]>=myLat)

					# test longitude
					passLon = (myLon <= pairs[i+1][0])
				
					if passLon and passLat:
						crossings += 1
		 					
		if crossings%2==1: 
			inProvince[fid] = True
		else:
			inProvince[fid] = False


### Print solution to terminal.
###--------------------------------------------------------------------------

solution = []
for i in inProvince:
	if inProvince[i] == True:
		solution.append([provinces[i]['provCode'], provinces[i]['provName']])

if len(solution)==0:
	print
	print 'No province found matching ', myLat, 'N, ', myLon, 'E.  '
	print 'This coordinate is either on land or it could be in one of these... '
	for i in inProvince:
		print provinces[i]['provCode'], '\t', provinces[i]['provName']
	print
	
elif len(solution) == 1:
	print
	print myLat, 'N, ', myLon, 'E -->  ', solution[0][0], '\t', solution[0][1]
	print
	
elif len(solution) > 1:
	print
	print 'Conflict between these provinces... '
	for i in solution:
		print solution[0][0], '\t', solution[0][1]
	print
		
