from agents.items import TResponseInputItem
import threading


class SessionService:
    _instance = None
    _lock = threading.Lock()


    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(SessionService, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance


    def __init__(self):
        if not self._initialized:
            self.sessions = {}
            self._initialized = True


    def get_session(self, session_id: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        
        return self.sessions[session_id]
    
    
    def add_session(self, session_id: str, item: TResponseInputItem):
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        self.sessions[session_id].append(item)
    
    
    def delete_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]