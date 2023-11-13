class Map:
    def __init__(self):
        self.list = []

    def add(self, object):
        self.list.append(object)

    def getObject(self, id):
        return self.list[id]
    
    def getNumber(self):
        return len(self.list)
    
    def clear(self):
        self.list = []
