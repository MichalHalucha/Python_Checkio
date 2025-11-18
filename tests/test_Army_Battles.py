import pytest

from src.Army_Battles import Army, Battle, Knight, Warrior, fight


@pytest.fixture
def warrior():
    return Warrior()


@pytest.fixture
def knight():
    return Knight()


@pytest.fixture
def battle():
    return Battle()


@pytest.fixture
def army_empty():
    return Army()


@pytest.fixture
def army_with_3_knights():
    army = Army()
    army.add_units(Knight, 3)
    return army


@pytest.fixture
def army_with_3_warriors():
    army = Army()
    army.add_units(Warrior, 3)
    return army


@pytest.fixture
def army_3():
    """Armia: 20 Warrior + 5 Knight."""
    army = Army()
    army.add_units(Warrior, 20)
    army.add_units(Knight, 5)
    return army


@pytest.fixture
def army_4():
    """Armia: 30 Warrior."""
    army = Army()
    army.add_units(Warrior, 30)
    return army


# ===================== TESTY KLAS =====================


def test_warrior_default_values(warrior):
    assert warrior.health == 50
    assert warrior.attack == 5
    assert warrior.is_alive is True


def test_knight_default_values(knight):
    assert knight.health == 50
    assert knight.attack == 7
    assert knight.is_alive is True
    assert isinstance(knight, Warrior)  # dziedziczenie


def test_is_alive_changes_with_health(warrior):
    assert warrior.is_alive is True
    warrior.health = 0
    assert warrior.is_alive is False
    warrior.health = -10
    assert warrior.is_alive is False


# ===================== TESTY FIGHT (1v1) =====================


def test_fight_warrior_vs_warrior(warrior):
    # używamy jednego fixture 'warrior' i tworzymy drugiego lokalnie
    w1 = warrior
    w2 = Warrior()
    result = fight(w1, w2)

    assert result is True
    assert w1.is_alive is True
    assert w2.is_alive is False


def test_fight_warrior_vs_knight(warrior, knight):
    result = fight(warrior, knight)

    assert result is False
    assert warrior.is_alive is False
    assert knight.is_alive is True


def test_fight_knight_vs_warrior(knight):
    w = Warrior()
    result = fight(knight, w)

    assert result is True
    assert knight.is_alive is True
    assert w.is_alive is False


# ===================== TESTY ARMII =====================


def test_add_units_creates_correct_number_of_units(army_empty):
    army_empty.add_units(Warrior, 5)
    assert len(army_empty.units) == 5
    assert all(isinstance(u, Warrior) for u in army_empty.units)


def test_add_units_order_fifo(army_empty):
    # pierwszy Warrior, potem dwóch Knight
    army_empty.add_units(Warrior, 1)
    army_empty.add_units(Knight, 2)

    assert isinstance(army_empty.units[0], Warrior)
    assert isinstance(army_empty.units[1], Knight)
    assert isinstance(army_empty.units[2], Knight)


# ===================== TESTY BATTLE (ARMIA vs ARMIA) =====================


def test_battle_small_armies(battle, army_with_3_knights, army_with_3_warriors):
    result = battle.fight(army_with_3_knights, army_with_3_warriors)

    # zgodnie z zadaniem: 3 Knight vs 3 Warrior → True
    assert result is True


def test_battle_large_armies(battle, army_3, army_4):
    result = battle.fight(army_3, army_4)

    # zgodnie z zadaniem: (20W + 5K) vs (30W) → False
    assert result is False


def test_battle_army1_starts_and_has_initiative(battle):
    """
    Sprawdzamy, że armia_1 ma przewagę startu (inicjatywy).
    Jeden Knight kontra jeden Warrior – Knight wygrywa,
    ale odwrócenie kolejności armii może zmienić wynik w innych konfiguracjach.
    """

    army_1 = Army()
    army_1.add_units(Knight, 1)

    army_2 = Army()
    army_2.add_units(Warrior, 1)

    result = battle.fight(army_1, army_2)
    assert result is True  # armia_1 wygrywa


def test_battle_empty_vs_non_empty(battle, army_empty, army_with_3_warriors):
    # pusta armia powinna przegrać z niepustą
    result = battle.fight(army_empty, army_with_3_warriors)
    assert result is False
