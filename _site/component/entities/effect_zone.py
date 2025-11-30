class EffectZone:

    def __init__(self, x1, y1, x2, y2, speed_debuff=0, life_debuff=0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.speed_debuff = speed_debuff
        self.life_debuff = life_debuff

    def is_inside(self, entity):
        return self.x1 <= entity.position.x <= self.x2 and self.y1 <= entity.position.y <= self.y2

    def apply_effect(self, entity):
        if self.is_inside(entity):
            entity.speed -= self.speed_debuff
            entity.life -= self.life_debuff
