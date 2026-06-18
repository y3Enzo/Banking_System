class User:
    def __init__(self, name, email, password, users_list):
        self._id = None
        self._name = name.title().strip()
        self._email = email.strip()
        self._password = password.strip()
        self._account_number = None
        for user in users_list: # Needed to get some others informations of user (if exists in the json)
            if (user["email"] == email) and (user["password"] == password):
                self._id = user["id"]
                self._account_number = user["account_number"]

    def check_atts(self):
        if not isinstance(self._name, str): return False
        if not "@" in self._email: return False
        if len(self._password) != 8: return False
        return True

    def get_balance():
        pass