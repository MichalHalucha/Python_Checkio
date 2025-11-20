class Warrior:
    def __init__(self):
        self.health = 50
        self.max_health = 50  # ⬅️ NEW: zapamiętujemy maksymalne HP
        self.attack = 5

    @property
    def is_alive(self):
        return self.health > 0


class Knight(Warrior):
    def __init__(self):
        super().__init__()
        self.health = 50
        self.max_health = 50  # ⬅️ dopasowane do faktycznego HP
        self.attack = 7


class Defender(Warrior):
    def __init__(self):
        super().__init__()
        self.health = 60
        self.max_health = 60  # ⬅️ max HP dla Defendera
        self.attack = 3
        self.defense = 2


class Vampire(Warrior):
    def __init__(self):
        super().__init__()
        self.health = 40
        self.max_health = 40  # ⬅️ max HP dla Vampira
        self.attack = 4
        self.vampirism = 50


class Lancer(Warrior):
    def __init__(self):
        super().__init__()
        self.health = 50
        self.max_health = 50  # ⬅️ max HP dla LANCERA
        self.attack = 6
        self.pierce = 50  # % obrażeń na jednostkę za celem


# ⬇️ NEW: HEALER
class Healer(Warrior):
    def __init__(self):
        super().__init__()
        self.health = 60
        self.max_health = 60  # ⬅️ max HP Healer’a
        self.attack = 0  # ⬅️ Healer nie atakuje

    def heal(self, ally):
        if ally and ally.is_alive:
            ally.health = min(ally.health + 2, ally.max_health)


def damage(attacker, defender):
    defense = getattr(defender, "defense", 0)
    return max(0, attacker.attack - defense)


def fight(unit_1, unit_2, behind_1=None, behind_2=None):
    while unit_1.is_alive and unit_2.is_alive:
        # === ATAK unit_1 ===
        dealt = damage(unit_1, unit_2)
        unit_2.health -= dealt

        # Vampirism leczenie
        if hasattr(unit_1, "vampirism") and dealt > 0:
            unit_1.health += dealt * unit_1.vampirism / 100
            if hasattr(unit_1, "max_health"):
                unit_1.health = min(unit_1.health, unit_1.max_health)

        # Lancer – przebijające obrażenia na jednostkę za celem
        if hasattr(unit_1, "pierce") and dealt > 0 and behind_2:
            behind_damage = dealt * unit_1.pierce / 100
            behind_2.health -= behind_damage

        # Healer za unit_1 leczy go po jego ataku
        if isinstance(behind_1, Healer):
            behind_1.heal(unit_1)

        if not unit_2.is_alive:
            break

        # === KONTRATAK unit_2 ===
        dealt = damage(unit_2, unit_1)
        unit_1.health -= dealt

        # Vampirism leczenie
        if hasattr(unit_2, "vampirism") and dealt > 0:
            unit_2.health += dealt * unit_2.vampirism / 100
            if hasattr(unit_2, "max_health"):
                unit_2.health = min(unit_2.health, unit_2.max_health)

        # Lancer – przebijające obrażenia na jednostkę za celem
        if hasattr(unit_2, "pierce") and dealt > 0 and behind_1:
            behind_damage = dealt * unit_2.pierce / 100
            behind_1.health -= behind_damage

        # Healer za unit_2 leczy go po jego ataku
        if isinstance(behind_2, Healer):
            behind_2.heal(unit_2)

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

            # jednostka stojąca BEZPOŚREDNIO za frontem w każdej armii
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
