import datetime

class SearchedItem():
    
    def __init__(self, title: str = None, work_id: str = None, price_min: int = None, price_max: int = None, 
                 proposales_count: int = None, client_id: str = None, description: str = None, 
                 start_at: datetime = None, end_at: datetime = None, desired_delivery_at: datetime = None, site: str=None):
        self.title = title
        self.work_id = work_id
        self.price_min = price_min
        self.price_max = price_max
        self.proposales_count = proposales_count
        self.client_id = client_id
        
        self.description = description
        self.start_at = start_at
        self.end_at = end_at
        self.desired_delivery_at = desired_delivery_at
        self.site = site

    def to_dict(self):
        return self.__dict__.copy()
    
    
    def merge(self, item):
        for key, value in self.__dict__.items():
            if item.__dict__[key] is None:
                continue
            self.__dict__[key] = item.__dict__[key]