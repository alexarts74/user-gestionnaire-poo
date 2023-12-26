from crm import User
import pytest
from tinydb import TinyDB, table
from tinydb.storages import MemoryStorage


@pytest.fixture
def setup_db():
    User.DB = TinyDB(storage=MemoryStorage)

@pytest.fixture
def user(setup_db):
    u = User(first_name="Patrice",
                last_name="Bellin",
                phone_number="0123456789",
                address="1 rue du chemin, 75001 Paris")

    u.save()
    return u


def test_full_name(user):
    assert user.fullname == "Patrice Bellin"


def test_first_name(user):
    assert user.first_name == "Patrice"


def test_exists(user):
    assert user.exists() is True


def test_not_exists(setup_db):
    user = User(first_name="Patrice", last_name="Bellin", phone_number="0123456789", address="1 rue du crement, 75001 Paris")
    assert user.exists() is False


def test_db_instance(user):
    assert isinstance(user.db_instance, table.Document)
    assert user.db_instance["first_name"] == "Patrice"
    assert user.db_instance["last_name"] == "Bellin"
    assert user.db_instance["phone_number"] == "0123456789"
    assert user.db_instance["address"] == "1 rue du chemin, 75001 Paris"


def test_not_db_instance(setup_db):
    user = User(first_name="Patrice", last_name="Bellin", phone_number="0123456789", address="1 rue du crement, 75001 Paris")
    assert user.db_instance is None


def test_check_phone_number(setup_db):
    user_good = User(first_name="Jean", last_name="jean", phone_number="0123456789", address="1 rue de paris, Paris")
    user_bad = User(first_name="Jean", last_name="jean", phone_number="abcdefg", address="1 rue de paris, Paris")

    with pytest.raises(ValueError) as err:
        user_bad._check_phone_number()

    assert "invalide" in str(err.value)

    user_good.save(validates_data=True)
    assert user_good.exists() == True




def test_check_name(setup_db):
    user_bad = User(first_name="", last_name="", phone_number="0123456789", address="1 rue de paris, Paris")
    user_good = User(first_name="john", last_name="john", phone_number="0123456789", address="1 rue de paris, Paris")

    with pytest.raises(ValueError) as err:
        user_bad._check_name()
    assert "Manque un prénom ou un nom" in str(err.value)

    user_good.save(validates_data=True)
    assert user_good.exists() == True


def test_delete(setup_db):
    user = User(first_name="john", last_name="john", phone_number="0123456789", address="1 rue de paris, Paris")
    user.save()

    first = user.delete()
    second = user.delete()

    assert len(first) > 0
    assert isinstance(first, list)

    assert len(second) == 0
    assert isinstance(second, list)


def test_save(setup_db):
    user_good = User(first_name="john", last_name="john", phone_number="0123456789", address="1 rue de paris, Paris")
    user_good_dup = User(first_name="john", last_name="john", phone_number="0123456789", address="1 rue de paris, Paris")

    first = user_good.save()
    second = user_good_dup.save()

    assert isinstance(first, int)
    assert isinstance(second, int)
    assert first > 0
    assert second == -1
