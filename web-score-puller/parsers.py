from FIRSTDataParser import FIRSTDataParser
import re
import copy

class RankParser(FIRSTDataParser):
    def __init__(self, event_data):
        super(RankParser, self).__init__(event_data, 'rankings.html')
        
    def data_table_matcher(self, tag):
        return self.is_table_with_first_row(tag, re.compile('Dataas of Match Number'))
    
    def get_ranks(self):
        content = self.request();
        data_table = content.find(self.data_table_matcher, recursive=False);
        return self.parse_table(data_table, 1);
    

class ScheduleParser(FIRSTDataParser):
    def __init__(self, event_data, data_path, first_line):
        super(ScheduleParser, self).__init__(event_data, data_path)
        self.first_line = first_line;
        
    def data_table_matcher(self, tag):
        return self.is_table_with_first_row(tag, re.compile(self.first_line))
    
    def get_schedule(self):
        content = self.request();
        data_table = content.find(self.data_table_matcher, recursive=False);
        return self.parse_table(data_table, 1);
    
    
class QualificationScheduleParser(ScheduleParser):
    def __init__(self, event_data):
        super(QualificationScheduleParser, self).__init__(event_data, 'schedulequal.html', 'Qualification Schedule')
        
class EliminationScheduleParser(ScheduleParser):
    def __init__(self, event_data):
        super(EliminationScheduleParser, self).__init__(event_data, 'scheduleelim.html', 'Elimination Schedule')
        
      
class ResultsParser(FIRSTDataParser):
    def __init__(self, event_data):
        super(ResultsParser, self).__init__(event_data, 'matchresults.html')
        
    def data_table_matcher(self, tag):
        return self.is_table_with_first_row(tag, re.compile('Dataas of Match Number'))
    
    def get_results(self):
        content = self.request();
        data_tables = content.find_all(self.data_table_matcher, recursive=False);
        qual_table = self.parse_table(data_tables[0], 2);
        elim_table = self.parse_table(data_tables[1], 2);
        
        data = copy.copy(qual_table['data']);
        for row in elim_table['data']:
            data.append(row[0:2]+row[3:11]);
        
        return {'headings': qual_table['headings'], 'data': data};
    