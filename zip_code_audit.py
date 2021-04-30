# Auditing Postal Codes

'''
this audits postal codes in a very similar process to street auditing

'''
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSM_FILE = "germantown.osm"
zip_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

zip_types = defaultdict(set)

expected_zip = {38138, 38139, 38183}

def audit_zip_codes(zip_types, zip_name, regex, expected_zip):
    m = regex.search(zip_name)
    if m:
        zip_type = m.group()
        if zip_type not in expected_zip:
             zip_types[zip_type].add(zip_name)

def is_zip_name(elem):
    return (elem.attrib['k'] == "addr:postcode")


def audit(filename, regex):
    for event, elem in ET.iterparse(filename, events=("start",)):
        if elem.tag == "way" or elem.tag == "node":
            for tag in elem.iter("tag"):
                if is_zip_name(tag):
                    audit_zip_codes(zip_types, tag.attrib['v'], regex, expected_zip)
    pprint.pprint(dict(zip_types))



    
audit(OSM_FILE, zip_type_re)


for zip_type, ways in zip_types.items(): 
        for name in ways:
            if "-" in name:
                name = name.split("-")[0].strip()
            if "TN " in name:
                name = name.split("TN ")[1].strip('TN ')
            elif len(str(name))>5:
                name=name[0:5]
            elif name.isdigit()==False:
                print ('OK')
            print (name)  

