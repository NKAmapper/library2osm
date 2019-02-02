#!/usr/bin/env python
# -*- coding: utf8

# library2osm 
# Converts librarys from BaseBibliotek feed "https://www.nb.no/baser/bibliotek/eksport/bb-full.xml" to osm format for import/update
# Usage: python library2osm.py > output_filename.osm


import cgi
import urllib2
import json
from bs4 import BeautifulSoup


version = "0.1.0"


transform = [
	('Hovedbiblioteket', ''),
	('Hovudbiblioteket', ''),
	('Bibliotek', 'bibliotek'),
	('Bok i butikk', 'bok i butikk'),
	('Skole', 'skole'),
	('Skule', 'skule'),
	('Avd', 'avd')
]


# Produce a tag for OSM file

def make_osm_line(key,value):

    if value:
		encoded_value = cgi.escape(value.encode('utf-8'),True)
		print ('    <tag k="%s" v="%s" />' % (key, encoded_value))


# Main program

if __name__ == '__main__':

	# Read county names

	filename = "https://register.geonorge.no/api/sosi-kodelister/fylkesnummer.json?"
	file = urllib2.urlopen(filename)
	county_data = json.load(file)
	file.close()

	county_names = {}
	for county in county_data['containeditems']:
		if county['status'] == "Gyldig":
			county_names[county['codevalue']] = county['label'].strip()

	# Load XML feed with library data

	filename = "https://www.nb.no/baser/bibliotek/eksport/bb-full.xml"
	file = urllib2.urlopen(filename)
	soup = BeautifulSoup(file, features="html.parser")
	file.close()

	# Produce OSM file header

	print ('<?xml version="1.0" encoding="UTF-8"?>')
	print ('<osm version="0.6" generator="library2osm v%s" upload="false">' % version)

	node_id = -20000

	# Loop all librarys and produce OSM file

	libraries = soup.find_all("record")

	for library in libraries:

		# Include Norwegian libraries only

		if not(library.find('stengt')) and (library.find('landkode')) and (library.find('landkode').get_text() == "no"):

			node_id -= 1

			# Get coordinates, if any

			coordinates = ""
			if library.find('lat_lon'):
				coordinates = library.find('lat_lon').get_text() 
				coordinates = coordinates.replace(", ", ",")

				if not(u"°" in coordinates) and not(" " in coordinates):
					coordinates_split = coordinates.split(",")
					latitude = coordinates_split[0]
					longitude = coordinates_split[1]
				else:
					latitude, longitude = ("0", "0")
			else:
				latitude, longitude = ("0", "0")

			print('  <node id="%i" lat="%s" lon="%s">' % (node_id, latitude, longitude))

			# Produce tags

			make_osm_line ("amenity", "library")
			make_osm_line ("ref:isil", "NO-" + library.find('bibnr').get_text().strip())

			library_type = library.find('bibltype').get_text()
			if ("FBI" in library_type) or (("FIL" in library_type) and not("FEN" in library_type)):  # Public libraries
				make_osm_line ("access", "yes")
			make_osm_line ("LIBRARY_TYPE", library.find('bibltype').get_text())

			name = library.find('inst').get_text()
			for word in transform:
				name = name.replace(word[0], word[1])
			name = name.replace("\n", ", ").replace(" - ,",",").replace(" ,",",").replace("  "," ").strip("-, ")
			make_osm_line ("name", name)

#			if library.find('inst_eng'):
#				make_osm_line ("name:en", library.find('inst_eng').get_text())

			# Contact information. The data owner has requested the e-mail address NOT to be included
	
			if library.find('url_hjem'):
				make_osm_line ("website", library.find('url_hjem').get_text().strip())
			if library.find('tlf'):
				make_osm_line ("phone", "+47 " + library.find('tlf').get_text().strip())

			# Produce address line, using visiting address if possible

			address = ""
			street = ""

			if library.find('vadr'):
				street = library.find('vadr').get_text()
				street = street.strip()
				if street:
					address = street + ", "

			if library.find('besadr'):
				bstreet = library.find('besadr').get_text()
				bstreet = bstreet.strip()
				if bstreet:
					make_osm_line ("BESØKSADRESSE", bstreet)
					if not(street):
						street = bstreet
						address = street + ", "
					else:
						make_osm_line ("VAREADRESSE", street)

			postcode = library.find('vpostnr').get_text()
			city = library.find('vpoststed').get_text()

			address = address + postcode + " " + city
			make_osm_line ("ADDRESS", address)

			# Use municipality number to discover county

			if library.find('kommnr'):
				county = county_names[ library.find("kommnr").get_text()[0:2] ]
				make_osm_line ("COUNTY", county)

			# Done with OSM library node

			print('  </node>')


	# Produce OSM file footer

	print('</osm>')
  
