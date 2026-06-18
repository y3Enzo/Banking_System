from user import User
from bank import Bank

def main():
    bank = Bank("Test", "data/users.json", "data/logs.json")
    user1 = User("a", "@email.com", "12345678", bank._users_list)
    if user1.check_atts():
        bank.create_account(user1)
        code = bank.get_code()
        bank.activate_account(user1._account_number, code=code, inserted_code=code) # Equal code variable to tests
    user2 = User("User 6", "user6@email.com", "pass0006", bank._users_list)
    if user2.check_atts(): pass

if __name__ == "__main__": main()