from collections import deque
import heapq

class FIFOQueue:
    def __init__(self):
        self.items = deque()
        
    def EMPTY(self):
        return len(self.items) == 0
        
    def TOP(self):
        return self.items[0] if not self.EMPTY() else None
        
    def POP(self):
        return self.items.popleft() if not self.EMPTY() else None
        
    def ADD(self, element):
        self.items.append(element)
        return self.items

class LIFOQueue:
    def __init__(self):
        self.items = []
        
    def EMPTY(self):
        return len(self.items) == 0
        
    def TOP(self):
        return self.items[-1] if not self.EMPTY() else None
        
    def POP(self):
        return self.items.pop() if not self.EMPTY() else None
        
    def ADD(self, element):
        self.items.append(element)
        return self.items

class PriorityQueue:
    def __init__(self):
        self.items = []
        
    def EMPTY(self):
        return len(self.items) == 0
        
    def TOP(self):
        return self.items[0] if not self.EMPTY() else None
        
    def POP(self):
        return heapq.heappop(self.items) if not self.EMPTY() else None
        
    def ADD(self, element):
        heapq.heappush(self.items, element)
        return self.items