# Longhurst-Province-Finder

This Python script takes as input latitude and longitude coordinates and returns the 
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
		
