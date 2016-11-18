import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint


OSMFILE =  "dublin_ireland.osm"
street_type_re = re.compile(r'\b\S+\.?$',re.IGNORECASE)


expected = ["Ave","Rd","Rd.","Roafd","St","st"]

mapping = { "Ave": "Avenue",
			"Rd": "Road",
			"Rd.": "Road",
			"Roafd": "Road",
			"St": "Street",
			"st": "Street",
			"St,": "Street"
			}

def audit_street_type(street_types, street_name):
	m = street_type_re.search(street_name)
	if m:
		street_type = m.group()
		#print street_type
		if street_type  in expected:
			street_types[street_type].add(street_name)

def is_street_name(elem):
	return (elem.attrib['k'] == "addr:street")




def audit(osmfile):
	osm_file = open(osmfile, "r")
	street_types = defaultdict(set)
	for event, elem in ET.iterparse(osm_file, events=("start",)):

		if elem.tag == "node" or elem.tag =="way":
			for tag in elem.iter("tag"):
				if is_street_name(tag):
					audit_street_type(street_types, tag.attrib['v'])
					#print tag.attrib['v']
	osm_file.close()
	return street_types

def update_name(name, mapping):
	m = street_type_re.search(name)
	#print m
	if m:
		street_type = m.group()
		#print street_type
		#print mapping.keys()

		if street_type in expected:
			name = re.sub(street_type_re,mapping[street_type],name)

	return name


def main():
	st_types = audit(OSMFILE)

	pprint.pprint(dict(st_types))

	for st_type, ways in st_types.iteritems():
		for name in ways:
			better_name = update_name(name, mapping)
			print name, "=>", better_name




if __name__ == '__main__':

	main()