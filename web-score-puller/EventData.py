
class EventData(object):

    def __init__(self, year, event_id):
        self.year = year;
        self.event_id = event_id;
        
    def data_url_prefix(self):
        return "/"+str(self.year)+"comp/Events/"+self.event_id+"/";