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


class Vampire(Warrior):
    def __init__(self):
        super().__init__()
        self.health = 40
        self.attack = 4
        self.vampirism = 50


class Lancer(Warrior):
    def __init__(self):
        super().__init__()
        self.health = 50
        self.attack = 6
        self.pierce = 50


def damage(attacker, defender):
    defense = getattr(defender, "defense", 0)
    return max(0, attacker.attack - defense)


def fight(unit_1, unit_2, behind_1=None, behind_2=None):
    while unit_1.is_alive and unit_2.is_alive:
        dealt = damage(unit_1, unit_2)
        unit_2.health -= dealt
        if hasattr(unit_1, "vampirism") and dealt > 0:
            unit_1.health += dealt * unit_1.vampirism / 100
        if hasattr(unit_1, "pierce") and dealt > 0 and behind_2:
            behind_damage = dealt * unit_1.pierce / 100
            behind_2.health -= behind_damage
        if not unit_2.is_alive:
            break
        dealt = damage(unit_2, unit_1)
        unit_1.health -= dealt
        if hasattr(unit_2, "vampirism") and dealt > 0:
            unit_2.health += dealt * unit_2.vampirism / 100
        if hasattr(unit_2, "pierce") and dealt > 0 and behind_1:
            behind_damage = dealt * unit_2.pierce / 100
            behind_1.health -= behind_damage
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

            behind_1 = (
                army_1.units[index_1 + 1] if index_1 + 1 < len(army_1.units) else None
            )
            behind_2 = (
                army_2.units[index_2 + 1] if index_2 + 1 < len(army_2.units) else None
            )

            result = fight(unit_1, unit_2, behind_1, behind_2)

            if result:
                index_2 += 1
            else:
                index_1 += 1

        return index_1 < len(army_1.units)
