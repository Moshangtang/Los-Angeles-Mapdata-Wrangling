
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from collections import defaultdict


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


mapping = { "St": "Street",
            "St.": "Street",
            "Rd.": "Road",
            "Rd": "Road",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "Pl": "Place",
            "Pl.": "Place",
            "Dr": "Drive",
            "Dr.": "Drive",
            "Ct": "Court",
            "Ct.": "Court",
            "PKWY": "Parkway",
            "Trl": "Trail",
            "Trl.": "Trail",
            "Sq": "Squre",
            "Sq.":"Squre",
            "Ln": "Lane",
            "Ln.": "Lane",
            "E": "East",
            "W": "West",
            "N": "North",
            "S": "South"
            }

def update_name(name, mapping):
    # I would like to use split to remove the second part of the name like" Paramount Blvd / MP 10.23"
    name = name.split('/')[0]
    for key in mapping:
        if key in name:
             name = re.sub(r'\b' + key + r'\b\.?', mapping[key], name)

    return name

def get_element(file_in):
    context = ET.iterparse(file_in,events=('start',))
    _,root = next(context)
    for _, element in context:
        yield element
        root.clear()

def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        node['id'] = element.attrib["id"]
        node['type'] = element.tag
        created = {"changeset": element.attrib["changeset"],
        "user": element.get("user"),
        "version": element.attrib["version"],
        "uid": element.get("uid"),
        "timestamp": element.attrib["timestamp"]}
        node['created'] = created
        if element.get('visible') is not None:
            node['visible'] = element.get('visible')
        try:
            pos = [float(element.attrib["lat"]), float(element.attrib["lon"])]
            node['pos'] = pos
        except:
            pass
        try:
            if element.tag == "node":
                address = {}
                for tag in element.iter("tag"):
                    if not problemchars.search(tag.attrib['k']):
                        tag_name = tag.attrib['k']
                        tag_value = tag.attrib['v']
                        if 'addr' in tag_name and len(tag_name.split(':'))==2:
                            add_key = tag_name.split(':')[-1]
                            if add_key == 'street':
                                address[add_key] = update_name(tag_value, mapping)
                            else:
                                address[add_key] = tag_value
                        elif tag_name == 'amenity':
                            node['amenity'] == tag_value
                        elif tag_name == 'cuisine':
                            node['cuisine'] = tag_value
                        elif tag_name == 'name':
                            node['name'] = update_name(tag_value, mapping)
                        elif tag_name =='phone':
                            node['phone'] = tag_value
                if len(address) >= 1:
                    node['address'] = address
        except:
            pass
        try:
            if element.tag == "way":
                node_refs = []
                for tag in element.iter("nd"):
                    node_refs.append(tag.attrib['ref'])
                if len(node_refs) >= 1:
                    node['node_refs'] = node_refs
        except:
            pass

        return node
    else:
        return None



def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    n=0
    with codecs.open(file_out, "w") as fo:
        for element in get_element(file_in):
            el = shape_element(element)
            if el:
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")






'''

def test():
    add_data = process_map('los_angeles.osm', True)
    #pprint.pprint(data)
    pprint.pprint(len(add_data))
    #pprint.pprint(add_data)

    post_data= []

    for i in add_data:
        if 'street' in i.keys():
            post_data.append(i['street'])

    pprint.pprint(len(post_data))
    pprint.pprint(post_data[:200])
'''


if __name__ == "__main__":
    process_map('sample.osm', True)
    pprint.pprint('Json file is ready!')