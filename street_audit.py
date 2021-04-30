import xml.etree.ElementTree as ET
import pprint
from collections import defaultdict
import re


OSM_FILE = "germantown.osm"

# Auditing Street Names

'''
first create a regex for the street names and store it in street_type_re. 
then create a default dictionary that will include sets of different street names.
finally audit the datafile and look for street names that have an ending that is different to
the values in the expected list.

'''



street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons","Freeway","Circle","Way","Highway", "Cove",
            "Terrace","South","East","West","North"]

# THIS mapping is for the updates that will occur
mapping = {
            " St ": " Street ",
            " St.": " Street ",
            " Rd.": " Road ",
            " Rd ": " Road ",
            " Rd": " Road ",
            " Ave ": " Avenue ", 
            " Ave.": " Avenue ",
            " Av ": " Avenue ", 
            " Dr ": " Drive ",
            " Dr.": " Drive",
            " Blvd ": " Boulevard ",
            " Blvd": " Boulevard",
            " Blvd.": " Boulevard",
            " Ct ": " Centre ",
            " Ctr": " Centre",
            " Pl ": " Place ",
            " Ln ": " Lane ",
            " Cir ": " Circle ",
            "Cv" : "Cove",
            " Wy": " Way ",
            " S ": " South ",
            " E ": " East ",
            " W ": " West ",
            " N ": "North"
}

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(filename):
    f = open(filename, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(filename, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
            elem.clear()        
    f.close()
    return street_types


def update_name(name, mapping):
    for key,value in mapping.items():
        if key in name:
            return name.replace(key,value)
    return name        



st_types = audit(OSM_FILE)

#pprint.pprint(dict(st_types))
for st_type, ways in st_types.items():
    for name in ways:
        better_name = update_name(name, mapping)
        print (name, "=>", better_name)
