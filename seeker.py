class seeker:
    def __init__(self, m):
        self.mymap = m.mapstate
        print(self.mymap)
        self.locx, self.locy = 1, 1
        self.records = []
        self.record_the_location(self.locx, self.locy)
    def movUp(self):
        if self.locy > 1:
            if self.record_the_location(self.locx, self.locy-1):
                self.locy = self.locy-1
                return True
        return False
    def movDown(self):
        if self.locy < self.mymap.shape[1]:
            if self.record_the_location(self.locx, self.locy+1):
                self.locy = self.locy+1
                return True
        return False
    def movLeft(self):
        if self.locx > 1:
            if self.record_the_location(self.locx-1, self.locy):
                self.locx = self.locx-1
                return True
        return False   
    def movRight(self):
        if self.locx < self.mymap.shape[2]:
            if self.record_the_location(self.locx, self.locy+1):
                self.locy = self.locy+1
                return True
        return False    
    def record_the_location(self, locx, locy):
        index = self.mymap.rows*(locx-1)+locy
        if index not in self.records:
            self.records.append(index)
            return True
            return False