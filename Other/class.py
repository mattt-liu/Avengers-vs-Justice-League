class Tower:
    
    def __init__(self, cost, damage, reload):
        self.cost   = int(cost)
        self.dmg    = int(damage)
        self.reload = int(reload)
        
    def __getitem__(self, i):
        self.feats = [self.cost, self.dmg, self.reload]
        return self.feats[i]
        
    def reloading(self):
        return 60 * self.reload
    
    def buy(self):
        return self.cost
    
class Npc:
    
    def __init__(self, health, damage, speed, place):
        self.hp    = int(health)
        self.speed = int(speed)
        self.dmg   = int(damage)
        self.x, self.y = place
        self.stop = False
        
    def __getitem__(self, i):
        # returns item in list that corresponds to entered index
        self.feats = [self.x, self.y, 25, 25]
        return self.feats[i]
    
    def stop(self, Bool):
        self.stop = Bool
        
    def move(self):
        if not self.stop:
            self.x -= self.speed // 12
        
    def hit(self, damage):
        # returns amount of health remaining if hit
        self.hp -= int(damage)
        if self.hp <= 0:
            return 0
        return self.hp

class Bullet:
    def __init__(self, point):
        self.v = 10
        self.x, self.y = point

    def __getitem__(self, i):
        self.points = [self.x, self.y]
        return self.points[i]
    
    def move(self):
        self.x += self.v
        self.points = [self.x, self.y]
        return tuple(self.points)
