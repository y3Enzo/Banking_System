# Banking_System

## Description
This project is a local banking system built in Python with OOP (Object-Oriented Programming) that's runs in terminal. The system uses a JSON file to store users and log processes like deposits. It also uses a .log file managed by the logging library to save logs such as system initialization and account creation, separating them from the JSON transaction logs.

## Important Behavior
NEVER DELETE A USER FROM THE USERS LIST: The system uses a template for JSON files, specifically in the users list. The list starts with a "ghost user" due to the search logic, which avoids using a for loop. If any user is deleted, the system will return an unexpected user or error during the search process.

CLOSED ACCOUNTS: If an account is closed, its email and password fields will be set to empty values (None in Python and null in JSON). Closed accounts cannot be reopened.

## Installation and Execution
Follow these steps to set up and run the project locally:

1. Clone the repository:
```bash
git clone https://github.com/y3Enzo/Banking_System.git
cd Banking_System
```

2. Create and activate a virtual environment (optional but recommended):

- Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

- MacOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```