import datetime

class SearchedItem():
    
    def __init__(self, title: str = None, work_id: str = None, price_min: int = None, price_max: int = None, 
                 proposales_number: int = None, client_id: str = None, description: str = None, 
                 start_at: datetime = None, end_at: datetime = None, desired_delivery_at: datetime = None):
        self.title = title
        self.work_id = work_id
        self.price_min = price_min
        self.price_max = price_max
        self.proposales_number = proposales_number
        self.client_id = client_id
        
        self.description = description
        self.start_at = start_at
        self.end_at = end_at
        self.desired_delivery_at = desired_delivery_at
        

    def to_dict(self):
        return self.__dict__.copy()