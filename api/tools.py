import os

class Tools:
    def __init__(self):
        return
    
    def get_router_mode(self):
        return(os.getenv('ROUTER_MODE'))