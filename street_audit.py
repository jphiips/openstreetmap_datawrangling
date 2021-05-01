import xml.etree.cElementTree as ET
import pprint
from collections import defaultdict
import re

dataset = "sample.osm"

street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
street_types = defaultdict(int)

#function audits for street types/name
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        street_types[street_type] += 1

#function prints sorted dictionary            
def print_sorted_dict(d, expression):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print (expression % (k, v))

#function defines street name
def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")

#function to audit the street types
def audit(filename):
    for event, elem in ET.iterparse(filename):
        if is_street_name(elem):
            audit_street_type(street_types, elem.attrib['v'])
    print(street_types, "%s: %d")
    return(street_types)

all_types = audit(dataset)
all_types

#the expected street types in the data
expected = ['Avenue', 'Boulevard', 'Broadway', 'Commons', 'Court', 'Cove','Drive', 'Lane', 'Park', 'Parkway',
            'Place', 'Road', 'Square', 'Street', 'Terrace', 'Trail', 'Turnpike', 'Creek','Way','Crossing','Lake',
            'North', 'South', 'East', 'West','Pike','Point']

#the mapping abbreviations to be used - Some common roads such as "Elkgate" were simply missing the term "Road" so these were added as well
abbr_mapping = {'Ave': 'Avenue',
                'Ave.': 'Avenue',
                'Ct': 'Court',
                'Cv': 'Cove',
                'Dr': 'Drive',
                'Pkwy': 'Parkway',
                'Rd': 'Road',
                'St': 'Street',
                'St.': 'Street',
                'Elkgate':'Road',
                'London' : 'Drive',
                'Chauncey' : 'Way'
                }

typo_full_names = {}

#function to audit street names
def audit_street_name(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if (all_types[street_type] < 20) and (street_type not in expected) and (street_type not in abbr_mapping):
            if street_type in typo_full_names:
                typo_full_names[street_type].append(street_name)
            else:
                typo_full_names.update({ street_type:[street_name] })

#audits names that will be changed
def audit_name(filename):
    for event, elem in ET.iterparse(filename):
        if is_street_name(elem):
            audit_street_name(street_types, elem.attrib['v'])    
    # print_sorted_dict(street_types)
    return typo_full_names

audit_name(dataset)

def audit_abbreviations(filename):
    problem_street_types = defaultdict(set)
    for event, elem in ET.iterparse(filename):
        if is_street_name(elem):
            expected_street_type(problem_street_types, elem.attrib['v'])
    return problem_street_types

def expected_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

#function to actually update the street names        
def update_street_name(name):
    street_type = name.split(' ')[-1]
    street_name = name.rsplit(' ', 1)[0]
    if street_type in abbr_mapping:
        name = street_name + ' ' + abbr_mapping[street_type]
    return name
    
def run_updates(filename):
    st_types = audit_abbreviations(dataset)
    for st_type, ways in st_types.items():
        for name in ways:
            better_name = update_street_name(name)
            if better_name != name:
                corrected_names[name] = better_name
    return corrected_names
            
corrected_names = {}           
corrected_names = run_updates(dataset)
print_sorted_dict(corrected_names, "%s: %s")
