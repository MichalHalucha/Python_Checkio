def trace(func):
    def wrapper(*args, **kwargs):
        cls = args[0].__class__.__name__
        print(f"[TRACE] {cls}.{func.__name__} called")
        return func(*args, **kwargs)

    return wrapper


class Warrior:
    @trace
    def __init__(self):
        self.health = 50
        self.max_health = 50
        self.attack = 5

    @property
    def is_alive(self):
        return self.health > 0

    def equip_weapon(self, weapon):
        self.max_health += weapon.health
        if self.max_health < 0:
            self.max_health = 0

        self.health += weapon.health
        if self.health > self.max_health:
            self.health = self.max_health
        if self.health < 0:
            self.health = 0

        # attack
        self.attack += weapon.attack
        if self.attack < 0:
            self.attack = 0

        if hasattr(self, "defense"):
            self.defense += weapon.defense
            if self.defense < 0:
                self.defense = 0

        if hasattr(self, "vampirism"):
            self.vampirism += weapon.vampirism
            if self.vampirism < 0:
                self.vampirism = 0

        if hasattr(self, "heal_power"):
            self.heal_power += weapon.heal_power
            if self.heal_power < 0:
                self.heal_power = 0


class Knight(Warrior):
    def __init__(self):
        super().__init__()
        self.health = 50
        self.max_health = 50
        self.attack = 7


class Defender(Warrior):
    def __init__(self):
        super().__init__()
        self.health = 60
        self.max_health = 60
        self.attack = 3
        self.defense = 2


class Vampire(Warrior):
    def __init__(self):
        super().__init__()
        self.health = 40
        self.max_health = 40
        self.attack = 4
        self.vampirism = 50  # %


class Lancer(Warrior):
    def __init__(self):
        super().__init__()
        self.health = 50
        self.max_health = 50
        self.attack = 6
        self.pierce = 50


class Healer(Warrior):
    def __init__(self):
        super().__init__()
        self.health = 60
        self.max_health = 60
        self.attack = 0
        self.heal_power = 2

    def heal(self, ally):
        if ally and ally.is_alive:
            ally.health = min(ally.health + self.heal_power, ally.max_health)


# ---------- WEAPONS ----------


class Weapon:
    def __init__(self, health=0, attack=0, defense=0, vampirism=0, heal_power=0):
        self.health = health
        self.attack = attack
        self.defense = defense
        self.vampirism = vampirism
        self.heal_power = heal_power


class Sword(Weapon):
    def __init__(self):
        super().__init__(health=5, attack=2)


class Shield(Weapon):
    def __init__(self):
        super().__init__(health=20, attack=-1, defense=2)


class GreatAxe(Weapon):
    def __init__(self):
        super().__init__(health=-15, attack=5, defense=-2, vampirism=10)


class Katana(Weapon):
    def __init__(self):
        super().__init__(health=-20, attack=6, defense=-5, vampirism=50)


class MagicWand(Weapon):
    def __init__(self):
        super().__init__(health=30, attack=3, heal_power=3)


# ---------- FIGHT LOGIC ----------


def damage(attacker, defender):
    defense = getattr(defender, "defense", 0)
    return max(0, attacker.attack - defense)


def fight(unit_1, unit_2, behind_1=None, behind_2=None):
    while unit_1.is_alive and unit_2.is_alive:
        dealt = damage(unit_1, unit_2)
        unit_2.health -= dealt

        if hasattr(unit_1, "vampirism") and dealt > 0:
            heal = int(dealt * unit_1.vampirism / 100)
            if heal > 0:
                unit_1.health = min(unit_1.health + heal, unit_1.max_health)

        if hasattr(unit_1, "pierce") and dealt > 0 and behind_2:
            base_pierce = dealt * unit_1.pierce / 100
            defense_behind = getattr(behind_2, "defense", 0)
            behind_damage = max(0, base_pierce - defense_behind)
            behind_2.health -= behind_damage

        if isinstance(behind_1, Healer):
            behind_1.heal(unit_1)

        if not unit_2.is_alive:
            break

        dealt = damage(unit_2, unit_1)
        unit_1.health -= dealt

        if hasattr(unit_2, "vampirism") and dealt > 0:
            heal = int(dealt * unit_2.vampirism / 100)
            if heal > 0:
                unit_2.health = min(unit_2.health + heal, unit_2.max_health)

        if hasattr(unit_2, "pierce") and dealt > 0 and behind_1:
            base_pierce = dealt * unit_2.pierce / 100
            defense_behind = getattr(behind_1, "defense", 0)
            behind_damage = max(0, base_pierce - defense_behind)
            behind_1.health -= behind_damage

        if isinstance(behind_2, Healer):
            behind_2.heal(unit_2)

    return unit_1.is_alive


# ---------- ARMIES & BATTLES ----------


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

    def straight_fight(self, army_1, army_2):
        while army_1.units and army_2.units:
            pairs = min(len(army_1.units), len(army_2.units))
            for i in range(pairs):
                fight(army_1.units[i], army_2.units[i])  # bez behind_1/behind_2
            army_1.units = [u for u in army_1.units if u.is_alive]
            army_2.units = [u for u in army_2.units if u.is_alive]
        return bool(army_1.units)
