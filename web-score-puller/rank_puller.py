#!/usr/bin/python

import glob, os, re, string, sys, traceback
from stat import *

from bs4 import BeautifulSoup
import httplib
import re
import json

conn = httplib.HTTPConnection("www2.usfirst.org")
conn.request("GET", "/2013comp/Events/ILCH/rankings.html")
#conn.request("GET", "/2014comp/events/ILIL/rankings.html")
response = conn.getresponse()
data = response.read()
conn.close()

def tag_string(tag):
    return re.sub(r'[^\x00-\x7F]+','', ''.join(tag.strings));

a = re.compile('Dataas of Match Number');
def data_table_matcher(tag):
    return tag.name == "table" and tag.tbody and tag.tbody.tr and tag.tbody.tr and a.match(tag_string(tag.tbody.tr.td))

soup = BeautifulSoup(data)
section1 = soup.find(class_ = "Section1");
data_table = section1.find(data_table_matcher, recursive=False);

def table_row_to_array(row):
    return map(lambda cell: tag_string(cell).strip(), row.find_all('td'));

def parse_table(table):
    table_rows = table.find_all('tr');
    
    heading_row = table_rows[1];
    headings = table_row_to_array(heading_row);
    data_rows = table_rows[2:-1];
    
    data = [];
    for row in data_rows:
        data_item = table_row_to_array(row);
        data.append(dict(zip(headings, data_item)))
    return data

print json.dumps(parse_table(data_table))