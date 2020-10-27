class Creature:

    def __init__(self, name, level, health_max):
        self.name = name
        self.level = level
        self.health = health_max
        self.health_max = health_max

    def __str__(self):
        return "Creature: {}\nLevel: {}\nHealth: {} / {}\n"\
            .format(self.name, self.level, self.health, self.health_max)

    def get_level(self):
        return self.level

    def new_level(self):
        self.level += 1
        self.health_max += 5
        self.health = self.health_max

    def attack(self, enemy):
        if self.level > enemy.level:
            enemy.undertake_attack((self.level - enemy.level) * 5)
        elif enemy.level > self.level:
            self.undertake_attack((enemy.level - self.level) * 5)

    def undertake_attack(self, damage):
        self.health -= damage

    def is_defeted(self):
        if self.health <= 0:
            return True
        return False


jozko = Creature("Jozko", 5, 10)
peter = Creature("Peter", 6, 30)
print(jozko)
print(peter)
jozko.attack(peter)
print(jozko)
print(peter)
