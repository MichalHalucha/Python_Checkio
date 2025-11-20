class Warrior:
    def __init__(self):
        self.health = 50
        self.attack = 5

    @property
    def is_alive(self):
        return self.health > 0


class Knight(Warrior):
    def __init__(self):
        super().__init__()
        self.attack = 7


class Defender(Warrior):
    def __init__(self):
        super().__init__()
        self.health = 60
        self.attack = 3
        self.defense = 2


def damage(attacker, defender):
    defense = getattr(defender, "defense", 0)
    return max(0, attacker.attack - defense)


def fight(unit_1, unit_2):
    # unit_1 zawsze atakuje pierwszy
    while unit_1.is_alive and unit_2.is_alive:
        unit_2.health -= damage(unit_1, unit_2)
        if not unit_2.is_alive:
            break
        unit_1.health -= damage(unit_2, unit_1)
    return unit_1.is_alive


class Army:
    def __init__(self):
        self.units = []

    def add_units(self, unit_class, count):
        for _ in range(count):
            self.units.append(unit_class())


class Battle:
    def fight(self, army_1, army_2):

        index_1 = 0
        index_2 = 0

        while index_1 < len(army_1.units) and index_2 < len(army_2.units):
            unit_1 = army_1.units[index_1]
            unit_2 = army_2.units[index_2]

            result = fight(unit_1, unit_2)

            if result:
                index_2 += 1
            else:
                index_1 += 1
        return index_1 < len(army_1.units)
