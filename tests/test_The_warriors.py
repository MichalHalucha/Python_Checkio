import pytest

from src.The_warriors import Knight, Warrior, fight

# --------- FIXTURES ---------


@pytest.fixture
def warrior():
    return Warrior()


@pytest.fixture
def knight():
    return Knight()


@pytest.fixture
def two_warriors():
    w1 = Warrior()
    w2 = Warrior()
    return w1, w2


@pytest.fixture
def warrior_and_knight():
    w = Warrior()
    k = Knight()
    return w, k


# --------- TESTY KORZYSTAJĄCE Z FIXTURES ---------


def test_warrior_default_values(warrior):
    assert warrior.health == 50
    assert warrior.attack == 5
    assert warrior.is_alive is True


def test_knight_default_values(knight):
    assert knight.health == 50
    assert knight.attack == 7
    assert knight.is_alive is True
    assert isinstance(knight, Warrior)


def test_is_alive_changes_with_health(warrior):
    assert warrior.is_alive is True

    warrior.health = 0
    assert warrior.is_alive is False

    warrior.health = -10
    assert warrior.is_alive is False


def test_fight_two_warriors(two_warriors):
    attacker, defender = two_warriors

    result = fight(attacker, defender)

    assert result is True
    assert attacker.is_alive is True
    assert defender.is_alive is False


def test_fight_warrior_vs_knight(warrior_and_knight):
    warrior, knight = warrior_and_knight

    result = fight(warrior, knight)

    assert result is False
    assert warrior.is_alive is False
    assert knight.is_alive is True


def test_knight_fights_twice(knight, warrior):
    result1 = fight(knight, warrior)
    assert result1 is True
    assert knight.is_alive is True
    assert warrior.is_alive is False

    new_warrior = Warrior()
    result2 = fight(knight, new_warrior)

    assert result2 in (True, False)
