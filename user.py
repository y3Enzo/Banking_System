from colorama import init, Fore, Style

# Colorama
init()

class User:
    def __init__(self, name, email, password, users_list):
        # Entered attributes
        self._name = name.title().strip()
        self._email = email.strip()
        self._password = password.strip()
        self._users_list = users_list

        # Predefined attributes that'll changes
        self._id = None
        self._account_number = None
        self._balance = 0
        self._is_active = False
        self._closed_account = False

    def check_atts(self): # Checks if the user entered valid data
        if not isinstance(self._name, str):
            return False
        if not "@" in self._email:
            return False
        if len(self._password) != 8:
            return False
        return True
