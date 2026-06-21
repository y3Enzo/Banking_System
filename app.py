from colorama import init, Fore, Style
from user import User
from bank import Bank
import logging

# Colorama
init()

# Logging
logger = logging.getLogger(__name__)

def menu_initial_page(bank):
    while True:
        try:
            print(f"{bank._name} Terminal System")
            print("[1] Create Account")
            print("[2] Enter Account")
            print("[3] Leave System")
            option = int(input("Select an option by its number: "))
            if option not in [1, 2, 3]:
                print(f"{Fore.RED}ERROR: Invalid option, try again{Style.RESET_ALL}")
                continue
            return option
        except ValueError:
            print(f"{Fore.RED}ERROR: The value entered is not a number between, try again{Style.RESET_ALL}")

def menu_account_creation(bank):
    while True:
        name = input("Name: ")
        email = input("E-mail: ")
        password = input("8 digits password: ")
        user = User(name, email, password, bank._users_list)
        if user._id != None:
            print(f"{Fore.RED}ERROR: Account already exists, try again{Style.RESET_ALL}")
            continue
        if not user.check_atts():
            print(f"{Fore.RED}ERROR: Wrong data entered, try again{Style.RESET_ALL}")
            continue
        bank.create_account(user)
        logger.info(f"Account ID: {user._id}, Number: {user._account_number} created")
        break

def menu_account_login(bank):
    while True:
        name = input("Name: ")
        email = input("E-mail: ")
        password = input("8 digits password: ")
        user = User(name, email, password, bank._users_list)
        user = bank.auth_user(user)
        if user._id == None:
            print(f"{Fore.RED}ERROR: Account not found, try again{Style.RESET_ALL}")
            continue
        if not user.check_atts():
            print(f"{Fore.RED}ERROR: Wrong data entered, try again{Style.RESET_ALL}")
            continue
        return user

def menu_account_logged(user):
    while True:
        print(f"Your balance: {user._balance}")
        print("[1] Change account status")
        print("[2] Make transactions")
        print("[3] Back")
        try:
            option = int(input("Select an option by its number: "))
            if option not in [1, 2, 3]:
                print(f"{Fore.RED}ERROR: Invalid option, try again{Style.RESET_ALL}")
                continue
            return option
        except ValueError:
            print(f"{Fore.RED}ERROR: The value entered is not a number between 1 and 3{Style.RESET_ALL}")
    
def menu_account_logged_change_status(user):
    while True:
        print(f"Actual status:", end=" ")
        print("active", end=" and ") if user._is_active else print("disabled", end=" and ")
        print("closed") if user._closed_account else print("open")
        print("[1] Activate account")
        print("[2] Disable account")
        print("[3] Close account")
        print("[4] Back")
        try:
            option = int(input("Select an option by its number: "))
            if option not in [1, 2, 3, 4]:
                print(f"{Fore.RED}ERROR: Invalid option, try again{Style.RESET_ALL}")
                continue
            return option
        except ValueError:
            print(f"{Fore.RED}ERROR: The value entered is not a number between 1 and 3{Style.RESET_ALL}")

def menu_account_logged_make_transaction():
    while True:
        print("[1] Deposit")
        print("[2] Withdraw")
        print("[3] Transfer")
        print("[4] Back")
        try:
            option = int(input("Select an option by its number: "))
            if option not in [1, 2, 3, 4]:
                print(f"{Fore.RED}Invalid option, try again{Style.RESET_ALL}")
                continue
            return option
        except ValueError:
            print(f"{Fore.RED}ERROR: The value entered is not a number between 1 and 3{Style.RESET_ALL}")
    
def menu_account_logged_deposit_or_withdraw():
    while True:
        try:
            amount = int(input("Amount: "))
            return amount
        except ValueError:
            print(f"{Fore.RED}ERROR: The value entered is not a number{Style.RESET_ALL}")
    
def menu_account_logged_transfer():
    while True:
        try:
            destine_account = input("Destine account: ")
            amount = int(input("Amount: "))
            return (destine_account, amount)
        except ValueError:
            print(f"{Fore.RED}ERROR: Invalid data entered{Style.RESET_ALL}")

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] | %(message)s",
        datefmt="%m-%d-%Y %H:%M:%S",
        handlers=[
            logging.FileHandler("data/system.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    bank = Bank("Bank", "data/users.json", "data/bank_logs.json")
    logger.info("Bank Initialized")
    while True:
        option = menu_initial_page(bank)

        if option == 1: # Create account
            menu_account_creation(bank)

        elif option == 2: # Enter account
            user = menu_account_login(bank)

            while True:
                logged_option = menu_account_logged(user)

                if logged_option == 1: # Change status
                    status_option = menu_account_logged_change_status(user)
                    if status_option != 4: # If don't want back (doing this to avoid code duplication when needs the verification code)
                        code = bank.get_code(user)
                        logger.info(f"Verification code number {code} sended to user ID {user._id}, account number {user._account_number}")
                        user_code = input("Verification code: ")

                        if status_option == 1: # Activate
                            if user._is_active:
                                print(f"{Fore.RED}ERROR: User account already active, leaving...{Style.RESET_ALL}")
                                continue
                            bank.activate_account(user, code, user_code)
                            if user._is_active:
                                logger.info(f"Account ID: {user._id}, Number: {user._account_number} activated")
                        elif status_option == 2: # Disable
                            if not user._is_active:
                                print(f"{Fore.RED}ERROR: User account already disabled, leaving...{Style.RESET_ALL}")
                                continue
                            bank.disable_account(user, code, user_code)
                            if not user._is_active:
                                logger.info(f"Account ID: {user._id}, Number: {user._account_number} disabled")
                        else: # Close
                            bank.close_account(user, code, user_code)
                            if user._closed_account:
                                logger.info(f"Account ID: {user._id}, Number: {user._account_number} closed")
                            break
                    else: # Back to account menu
                        continue
                elif logged_option == 2: # Make transactions
                    transaction_option = menu_account_logged_make_transaction()
                    
                    if transaction_option == 1: # Deposit
                        amount = menu_account_logged_deposit_or_withdraw()
                        bank.deposit(user, amount)
                    elif transaction_option == 2: # Withdraw
                        amount = menu_account_logged_deposit_or_withdraw()
                        bank.withdraw(user, amount)
                    elif transaction_option == 3: # Transfer
                        data = menu_account_logged_transfer()
                        bank.transfer(user, data[0], data[1])
                    else: # Back to account menu
                        continue
                else: # Break the loop to run the initial page
                    break
            continue
        
        else: # Leave system
            logger.info("Bank closed")
            break
    return

if __name__ == "__main__":
    main()