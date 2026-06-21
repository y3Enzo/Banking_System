from colorama import init, Fore, Style
from datetime import datetime
from pathlib import Path
from random import randint
import json

# Colorama
init()

# Datetime
def get_time():
    now = datetime.now()
    return now.strftime("%m/%d/%y %H:%M:%S")

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
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            if isinstance(e, FileNotFoundError):
                print(f"{Fore.RED}ERROR: File not found in {filepath}, an empty file will be created at the destination{Style.RESET_ALL}")
                data_folder = Path("data")
                data_folder.mkdir(parents=True, exist_ok=True)

            with open(filepath, "w", encoding="utf-8") as file:
                template = self.get_template(filepath)
                json.dump(self.get_template(filepath), file, indent=4, ensure_ascii=False)
                return template

    def get_template(self, filepath):
        if filepath != self._logs_filepath and filepath != self._users_filepath:
            return
        
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
        
        if filepath == self._users_filepath:
            return users_list_template
        else:
            return logs_template

    def create_account(self, user):
        if user._id != None: # If the user exists
            return
        number = ""
        for _ in range(8):
            number += str(randint(0,9))
        user._account_number = number
        user._id = self._users_list[len(self._users_list) - 1]["id"] + 1
        user_data = {
        "id": user._id,
        "name": user._name.title(),
        "email": user._email,
        "password": user._password,
        "account_number": number,
        "balance": 0,
        "is_active": False,
        "closed": False
        }
        log = {
            "account_id": user._id,
            "time": get_time()
        }
        self._users_list.append(user_data)
        self._logs["accounts_creation"].append(log)
        self.write_json(self._users_list, self._users_filepath)
        self.write_json(self._logs, self._logs_filepath)

    def get_code(self, user):
        code = ""
        for _ in range(6):
            code += str(randint(0, 9))
        
        log = {
            "account_id": user._id,
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
        else:
            return True
        
    def close_account(self, user, code, inserted_code):
        if not self.check_key(code, inserted_code):
            return
        
        self._users_list[user._id]["email"] = None
        self._users_list[user._id]["password"] = None
        self._users_list[user._id]['closed'] = True
        user._email = None
        user._password = None
        user._closed_account = True
        self.write_json(self._users_list, self._users_filepath)

        log = {
        "account_id": user._id,
        "time": get_time()
        }
        self._logs["accounts_closing"].append(log)
        self.write_json(self._logs, self._logs_filepath)

    def activate_account(self, user, code, inserted_code):
        if not self.check_key(code, inserted_code):
            return
        
        self._users_list[user._id]['is_active'] = True
        user._is_active = True
        self.write_json(self._users_list, self._users_filepath)

    def disable_account(self, user, code, inserted_code):
        if not self.check_key(code, inserted_code):
            return
        
        self._users_list[user._id]['is_active'] = False
        user._is_active = False
        self.write_json(self._users_list, self._users_filepath)

    def auth_user(self, user):
        for existing_user in user._users_list:
            if existing_user["email"] != user._email and existing_user["password"] != user._password:
                continue
            user._id = existing_user["id"]
            user._account_number = existing_user["account_number"]
            user._balance = existing_user["balance"]
            user._is_active = existing_user["is_active"]
            user._closed_account = existing_user["closed"]
            break
        return user

    # Transactions
    def deposit(self, user, amount):
        if not user._is_active:
            return
        if user._closed_account:
            return
        if amount < 0:
            return
        
        self._users_list[user._id]["balance"] += amount
        user._balance += amount
        log = {
            "account_id": user._id,
            "amount": amount,
            "time": get_time()
        }
        self._logs["deposits"].append(log)
        self.write_json(self._users_list, self._users_filepath)
        self.write_json(self._logs, self._logs_filepath)

    def withdraw(self, user, amount):
        if not user._is_active:
            return
        if user._closed_account:
            return
        if amount < 0 or amount > user._balance:
            return
        
        self._users_list[user._id]["balance"] -= amount
        user._balance -= amount
        log = {
            "account_id": user._id,
            "amount": amount,
            "time": get_time()
        }
        self._logs["withdraws"].append(log)
        self.write_json(self._users_list, self._users_filepath)
        self.write_json(self._logs, self._logs_filepath)

    def transfer(self, user, destine_user, amount):
        if not user._is_active or not destine_user._is_active:
            return
        if user._closed_account or destine_user._closed_account:
            return
        if amount < 0 or amount > user._balance:
            return

        self._users_list[user._id]["balance"] -= amount
        user._balance -= amount
        self._users_list[destine_user._id]["balance"] += amount
        destine_user._balance += amount
        log = {
            "sender_account_id": user._id,
            "recipient_account_id": destine_user._id,
            "amount": amount,
            "time": get_time()
        }
        self._logs["transfers"].append(log)
        self.write_json(self._users_list, self._users_filepath)
        self.write_json(self._logs, self._logs_filepath)
