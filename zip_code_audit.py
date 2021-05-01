import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

dataset = "sample.osm"

zip_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
zip_types = defaultdict(set)

expected_zip = {'38138', '38139', '38183'}

def audit_zip_codes(zip_types, zip_name, regex, expected_zip):
    m = regex.search(zip_name)
    if m:
        zip_type = m.group()
        if zip_type not in expected_zip:
             zip_types[zip_type].add(zip_name)

def is_zip_name(elem):
    return (elem.attrib['k'] == "addr:postcode")

#function to perform audit on the zip code data
def audit(filename, regex):
    for event, elem in ET.iterparse(filename, events=("start",)):
        if elem.tag == "way" or elem.tag == "node":
            for tag in elem.iter("tag"):
                if is_zip_name(tag):
                    audit_zip_codes(zip_types, tag.attrib['v'], regex, expected_zip)
    pprint.pprint(dict(zip_types))

 
audit(dataset, zip_type_re)

#audit of zip codes shows a few zip codes which are not part of the Germantown area. 
#the decidion was made to not clean this part of the dataset - the post codes represent neighboring areas
