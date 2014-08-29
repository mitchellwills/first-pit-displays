from EventData import EventData
from parsers import RankParser, QualificationScheduleParser, EliminationScheduleParser, ResultsParser
import json
import SimpleHTTPServer
import SocketServer
import time

current_milli_time = lambda: int(round(time.time() * 1000))

updateDelay = 10000;#in ms


def update():
    try:
        print 'updated'
        ranks = rank_parser.get_ranks();
        schedule = {'qual': qual_schedule_parser.get_schedule(), 'elim': elim_schedule_parser.get_schedule()};
        results = results_parser.get_results();
        data = {'ranks': ranks, 'schedule': schedule, 'results': results};
        data_file = open('data.json','w');
        data_file.write(json.dumps(data));
        data_file.close();
        print 'updating'
    except:
        print 'error updating'
    

if __name__ == '__main__':
    event_data = EventData(2014, 'MAWOR');
    
    rank_parser = RankParser(event_data);
    qual_schedule_parser = QualificationScheduleParser(event_data);
    elim_schedule_parser = EliminationScheduleParser(event_data);
    results_parser = ResultsParser(event_data);
    
    update();
    
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", 8000), Handler)
    lastUpdate = 0;
    while True:
        httpd.handle_request()
        if current_milli_time()>lastUpdate+updateDelay:
            lastUpdate = current_milli_time();
            update();