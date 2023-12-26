import re
import string
from tinydb import TinyDB, where
from pathlib import Path

class User:

    DB = TinyDB(Path(__file__).resolve().parent / "db.json", indent=4)

    def __init__(self, first_name: str, last_name: str, phone_number: str="", address: str=""):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address


    def __str__(self):
        return f"{self.fullname} - {self.phone_number} - {self.address}"


    def __repr__(self):
        return f"User({self.first_name}, {self.last_name})"


    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"


    @property
    def db_instance(self):
        return User.DB.get((where('first_name') == self.first_name) & (where('last_name') == self.last_name))


    def _check(self):
        self._check_name
        self._check_phone_number


    def _check_phone_number(self):
        phone_number = re.sub(r"[+()\s]*", "", self.phone_number)
        if len(phone_number) < 10 or not phone_number.isdigit():
            raise ValueError(f"Numéro de téléphone invalide {self.phone_number}")


    def _check_name(self):
        if not (self.first_name and self.last_name):
            raise ValueError("Manque un prénom ou un nom")

        special_caracthere = string.punctuation + string.digits

        for caracthere in self.first_name + self.last_name:
            if caracthere in special_caracthere:
                raise ValueError(f"Caractère spécial interdit dans le nom : '{caracthere}'")


    def exists(self):
        return bool(self.db_instance)


    def delete(self) -> list[int]:
        if self.exists():
            return User.DB.remove(doc_ids=[self.db_instance.doc_id])
        return []


    def save(self, validates_data=False):
        if validates_data:
            self._check()

        if self.exists():
            return -1
        else:
            return User.DB.insert(self.__dict__)


def get_all_users():
    return [User(**user) for user in User.DB.all()] # Egale a créer liste vide et incrementer
    # for user in User.DB.all():
    #     each_user = User(**user) #Débaler le dictionnaire
    #     print(each_user.first_name)

def add_to_list():
    liste = [1, 2]
    good_liste = liste.append(3)
    print(good_liste)

if __name__ == "__main__":
    # get_all_users()
    pierre = User("Pierre", "Perrot", "0123456789", "1 rue de paris 75009")
    print(pierre)
    print(pierre.exists())
