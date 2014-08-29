import httplib
import re
from bs4 import BeautifulSoup

class FIRSTDataParser(object):

    def __init__(self, event_data, data_path):
        self.event_data = event_data;
        self.data_path = data_path;
        
    def request(self):
        conn = httplib.HTTPConnection("www2.usfirst.org")
        conn.request("GET", self.event_data.data_url_prefix()+self.data_path)
        response = conn.getresponse()
        data = response.read()
        conn.close()

        soup = BeautifulSoup(data)
        section1 = soup.find(class_ = "Section1");
        return section1;
        
    def is_table(self, tag):
        return tag.name == "table";
    
    def is_table_with_first_row(self, tag, first_row_matcher):
        if not self.is_table(tag):
            return False;
        if tag.tbody:
            row_container = tag.tbody;
        else:
            row_container = tag;
        
        if row_container.tr:
            return first_row_matcher.match(self.tag_string(row_container.tr));
        return False;
        
    
    def tag_string(self, tag):
        return re.sub(r'[^\x00-\x7F]+','', ''.join(tag.strings)).strip();
    

    def parse_table(self, table, skip_rows):
        table_rows = table.find_all('tr');
        
        heading_row = table_rows[skip_rows];
        headings = self.table_row_to_array(heading_row);
        
        data_rows = table_rows[skip_rows+1:len(table_rows)];

        data = [];
        for row in data_rows:
            data_item = self.table_row_to_array(row);
            data.append(data_item)

        return {'headings': headings, 'data': data};
    
    def table_row_to_array(self, row):
        return map(lambda cell: self.tag_string(cell).strip(), row.find_all('td'));