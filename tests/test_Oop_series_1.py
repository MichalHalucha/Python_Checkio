import pytest

from src.Oop_series_1 import Car, my_car


@pytest.fixture
def car():
    return Car()


@pytest.fixture
def shared_car():
    return my_car


def test_car_instance(car):
    assert isinstance(car, Car)


@pytest.mark.parametrize("obj", [my_car])
def test_my_car_is_car_instance(obj):
    assert isinstance(obj, Car)


@pytest.mark.parametrize("factory", ["car", "shared_car"])
def test_all_car_fixtures_are_instances(request, factory):
    obj = request.getfixturevalue(factory)
    assert isinstance(obj, Car)
