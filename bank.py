from colorama import init, Fore, Style
from datetime import datetime
from random import randint
import json

# Colorama
init()

# Datetime
def get_time():
    now = datetime.now()
    return now.strftime("%d/%m/%y %H:%M:%S")

class Bank:
    def __init__(self, name, users_filepath, logs_filepath): # For now name is useless, but filepaths are importants
        self._name = name.title().strip()
        self._users_filepath = users_filepath.strip()
        self._logs_filepath = logs_filepath.strip()
        self._users_list = self.load_json(users_filepath)
        self._logs = self.load_json(logs_filepath)

    def write_json(self, content, filepath):
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(content, file, indent=4, ensure_ascii=False)
    
    def load_json(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"{Fore.RED}ERROR: File not found in {filepath}, an empty file will be created at the destination{Style.RESET_ALL}")
            with open(filepath, "w", encoding="utf-8") as file:
                template = self.get_template()
                json.dump(template, file, indent=4, ensure_ascii=False)
                return template

    def get_template(self, filepath):
        logs_template = {
            "verification_codes": [
                {
                    "account_id": 0,
                    "code": "",
                    "time": ""
                }
            ],
            "deposits": [
                {
                    "account_id": 0,
                    "amount": 0,
                    "time": ""
                }
            ],
            "withdraws": [
                {
                    "account_id": 0,
                    "amount": 0,
                    "time": ""
                }
            ],
            "transfers": [
                {
                    "sender_account_id": 0,
                    "recipient_account_id": 0,
                    "amount": 0,
                    "time": ""
                }
            ],
            "accounts_creation": [
                {
                    "account_id": 0,
                    "time": ""
                }
            ],
            "accounts_closing": [
                {
                    "account_id": 0,
                    "time": ""
                }
            ]
        }
        users_list_template = [
            {
                "id": 0,
                "name": "",
                "email": "",
                "password": "",
                "account_number": "",
                "balance": 0,
                "is_active": False,
                "closed": False
            }
        ]
        return users_list_template if filepath == self._users_filepath else logs_template

    def create_account(self, user):
        if user._id != None: return # Return if the user exists
        number = ""
        for _ in range(8):
            number += str(randint(0,9))
        user._account_number = number
        user_data = {
        "id": len(self._users_list),
        "name": user._name.title(),
        "email": user._email,
        "password": user._password,
        "account_number": number,
        "balance": 0,
        "is_active": False,
        "closed": False
        }
        log = {
            "account_id": len(self._users_list),
            "time": get_time()
        }
        self._users_list.append(user_data)
        self._logs["accounts_creation"].append(log)
        self.write_json(self._users_list, self._users_filepath)
        self.write_json(self._logs, self._logs_filepath)

    def get_code(self):
        id = len(self._users_list) - 1
        code = ""
        for _ in range(6):
            code += str(randint(0, 9))
        
        log = {
            "account_id": id,
            "code": code,
            "time": get_time()
        }
        self._logs["verification_codes"].append(log)
        self.write_json(self._logs, self._logs_filepath)
        return code

    @staticmethod
    def check_key(key, inserted_key):
        if key != inserted_key:
            return False
        return True
        
    def close_account(self, number, code, inserted_code):
        if not self.check_key(code, inserted_code): return
        number = number.strip()
        id = self.get_id_by_account_number(number)
        self._users_list[id]['closed'] = True
        self.write_json(self._users_list, self._users_filepath)

        logs = self._load_json(self._logs_filepath)
        log = {
        "account_id": id,
        "time": get_time()
        }
        logs["accounts_closing"].append(log)
        self.write_json(logs, self._logs_filepath)

    def activate_account(self, number, code, inserted_code):
        if not self.check_key(code, inserted_code): return
        number = number.strip()
        id = self.get_id_by_account_number(number)
        self._users_list[id]['is_active'] = True
        self.write_json(self._users_list, self._users_filepath)

    def disable_account(self, number, code, inserted_code):
        if not self.check_key(code, inserted_code): return 
        number = number.strip()
        id = self.get_id_by_account_number(number)
        self._users_list[id]['is_active'] = False
        self.write_json(self._users_list, self._users_filepath)

    def get_id_by_account_number(self, account_number):
        id = 0
        account_number = account_number.strip()
        for user in self._users_list:
            if not account_number in user["account_number"]: id += 1
            else: return id