"""Using OOP, implement a banking application that meets the following user requirements:
User can sign up / Register - 10 Marks
User can log in - 10 Marks.
User can deposit funds - 10 Marks.
gUser can Transfer Fund to another account - 10 Marks.
User can view Transaction History - 10 Marks.
User can check balance - 10 Marks.
Verbose Git commits - 10 Marks.
Comments and Docstrings - 10 Marks.
Code Readability - 10 Marks
Submission before deadline (Bonus) - 10 Marks.
You MAY use PayStack API to mock the transactions."""


"""importing the relevant libraries"""

# from bankcustomer import Customer


"""Create the Customer class with the relevant attributes:"""




from dataclasses import dataclass
from string import digits
from datetime import datetime
import random
import uuid


"""Class representing a customer.

    Attributes:
        history (dict): a dictionary that contains the transaction history of the customer
        trans_id (int): an integer representing the id of the current transaction

    Instance Attributes:
        firstName (str): first name of the customer
        lastName (str): last name of the customer
        phoneNo (int): phone number of the customer
        email (str): email address of the customer
        gender (str): gender of the customer
        dateOfBirth (datetime): date of birth of the customer
        occupation (str): occupation of the customer
        address (str): address of the customer
        __balance (int): current balance of the customer
        transaction (list): a list that contains the details of each transaction made by the customer
    """

@dataclass
class Customer:
    
    history = dict()
    trans_id = 0
    
    # def __init__(self, firstName:str, lastName:str, phoneNo:int, email:str, address:str, balance=0) -> None:
    firstName: str
    lastName: str
    phoneNo: int
    email: str
    gender: str
    dateOfBirth: datetime
    occupation: str
    address: str
    # __balance: int = 0 #Dataclass field cannot use private fields
    __balance = 0
    transaction = []
    
        # Return the string representation of the customer object.
    def __str__(self) -> str:
        fullName = f"{self.firstName} {self.lastName}"
        fullName = lambda first, last: first + " " + last
        return f"{fullName(self.firstName, self.lastName)} \t {self.phoneNo} \t {self.email} \t {self.gender} \t {self.dateOfBirth} \t {self.occupation} \t {self.address}"
    
    
    """Update the balance of the customer after a transaction.
        Args:
            type (str): the type of the transaction (deposit, withdrawal or transfer)
            amount (int): the amount of the transaction

        Raises:
            ValueError: if the transaction type is invalid or if the customer has insufficient funds for withdrawal or transfer
    
    """    
    def updateBalance(self, type, amount):
        """Updates the balance for deposit or credit transactions"""
        if type == "deposit":
            self.__balance += amount
        elif type == "withdrawal":
            if self.__balance <= amount:
                print("Insufficient funds")
                raise ValueError("Insufficient funds")
            else:
                self.__balance -= amount
        
        elif type == "transfer":
            if self.__balance <= amount:
                print("Insufficient funds")
                raise ValueError("Insufficient funds")
            else:
                recipient = input("Enter recipient's account number:  ")
                self.__balance -= amount
        
        else:            
            print("Invalid transaction type")
            return
        
        self.transaction.append({"type": type, "amount": amount, "balance": self.__balance, "time": datetime.now()})
    
    
    """Update the transaction history of the customer.
        Args:
            date (datetime): the date of the transaction
            type (str): the type of the transaction (deposit, withdrawal or transfer)
            amount (int): the amount of the transaction
    """    
    @classmethod
    def updateHistory(cls, date, type, amount):
        """Updates the transaction history of the customer"""
        accountNumber = random.choices(digits, k=10)
        cls.__setattr__("account_number", accountNumber)
        cls.history[f"{date}"] = {"type": type, "amount": amount, "balance": cls.balance}
    
    @property
    def getBalance(self): #Returns customer's balance
        return self.__balance
    
    def viewHistory(self):
        """Displays the transaction history of a customer"""
        history = ""
        for transadate, details in self.history.items():
            history += f"{transadate} \t {details['type']} \t {details['amount']} \t {details['balance']}\n"
        print(history)
        return history
    
    def generateAccount(self):
        """Generates an account number for a customer"""
        while True:
            accountNumber = str(uuid.uuid4().int)[:10]
            if accountNumber not in Bank.customers:
                self.__setattr__("account_number", accountNumber)
                return self.account_number

@dataclass
class Bank:
    bankName = "Point World Bank"

    customers = {}      # dictionary to store customer accounts and details
    balance: int = 0    # default bank balance
    usernames = {}      # dictionary to store customer usernames

    def deposit(self, account, amount):
        """Credits a customer's account with a given amount"""
        customer = self.customers[account]
        customer.updateBalance("deposit", amount)

    def withdrawal(self, account, amount):
        """Debits a customer's account"""
        customer = self.customers[account]
        customer.updateBalance("withdrawal", amount)

    def transfer(self, account, amount):
        """Debits a customer's account and transfers the amount to recipient's account"""
        customer = self.customers[account]
        customer.updateBalance("transfer", amount)

    def viewHistory(self, account):
        """Displays the transaction history of a customer"""
        if account in self.customers:
            customer = self.customers[account]
            customer.viewHistory()
        else:
            print("Account does not exist")
   
    @classmethod
    def signUp(cls, firstName, lastName, phoneNo, email, gender, dateOfBirth, occupation, address):
        """creates a new customer account"""
        customer = Customer(firstName, lastName, phoneNo,
                            email, gender, dateOfBirth, occupation, address)
        accountNumber = customer.generateAccount()
        cls.customers[f'{accountNumber}'] = customer
        return customer

    @classmethod
    def login(cls, arr):
        """Logs in a customer"""
        email = input("Email:  ")
        password = input("Password:  ")

        if email in arr and password in arr:
            print("\nLogin successful")
            return True
        else:
            print("\nInvalid login details")
            return False

#=============MAIN PROGRAM================
if __name__ == '__main__':
    running = True    #running is set to true to keep the program running
    transact = False    #transact is set to false to prevent the program from skipping the login process
    pointWorld = Bank() #object of the class Bank created
    loginDetail = []    # List to hold login details
    print("\n")
    print("WELCOME TO POINT WORLD BANK".center(60, "="))

    while running:
        print("\nPress a number between 1 and 7 that corresponds to the operation you wish to perform\n")
        operation = input(
            "1. Sign-up \n2. Check Balance \n3. Deposit \n4. Withdrawal \n5. Transfer \n6.Transaction History \n7.Exit\n") # Prompt user to select an operation

        if operation not in "1234567":  # Check if the input is valid
            print("\nWrong Entry. \nPlease enter a number between 1 and 7")
            continue
        else:
            if operation == "1":
                transact = True
                while transact:
                    print("\nThank you for choosing Point World. Please walk with me\n")
                    email = input("Email:  ")   # Email is used as username
                    if email in loginDetail:    # Check if the email already exist
                        print("\nUser already exist, please login")
                        break
                    loginDetail.append(email)   # Add email to loginDetail list
                    firstName = input("First Name:  ")  # Prompt user to enter first name
                    lastName = input("Last Name:  ")    # Prompt user to enter last name
                    phoneNo = input("Phone Number: ")   # Prompt user to enter phone number
                    dateOfBirth = input("Date of Birth:  ") # Prompt user to enter date of birth]
                    gender = input("Gender:  ") # Prompt user to enter gender
                    occupation = input("Occupation: ")  # Prompt user to enter occupation
                    address = input("Address:  ") # Prompt user to enter address
                    password = input("Password:  ") # Prompt user to enter password
                    loginDetail.append(password)    # Add password to loginDetail list
                    balance = int(input("Opening Balance (min: #1000):  ")) # Prompt user to enter opening balance

                    try:    
                        if len(firstName) > 3 and len(lastName) > 3 and len(phoneNo) > 3 and ("@" in email) and dateOfBirth and gender and occupation and len(address) > 3 and balance: # Check if the inputs are valid
                            if balance >= 1000: # Check if the opening balance is at least #1000
                                customer = Customer(
                                    firstName, lastName, phoneNo, email, gender, occupation, address, balance)  # Create a new customer object
                                accountNumber = customer.generateAccount()  # Generate an account number for the customer
                                if accountNumber:   # Check if the account number is generated
                                    pointWorld.customers.update(
                                        {accountNumber: customer})  # Add the customer to the customers dictionary
                                    # pointWorld.customers[f'{accountNumber}'] = customer
                                    print(
                                        f"\nCongratulations {firstName} {lastName}! Your account has been created successfully. Your account number is {accountNumber}. Please keep it safe")
                                    print("\n", pointWorld.customers.items())
                                    pointWorld.deposit(accountNumber, balance)  # Deposit the opening balance
                                    print(
                                        f"\nYour account has been credited with #{balance}. Your current balance is #{customer.getBalance}")
                                    print("\nPlease login to continue")
                                    transact = False    
                                    break   # Break out of the loop

                            else:
                                print("Opening balance must be at least #1000")
                                continue
                        else:
                            print("Invalid entry. Please try again")
                            continue
                    except ValueError:
                        print("Invalid entry")
                        break

            elif operation == "2":  # Check balance
                transact = True
                if not pointWorld.login(loginDetail):   # Check if the user is logged in
                    continue
                while transact:
                    print("\nPress 0 to cancel\n")
                    accountNumber = input("Enter your account number:  ")   # Prompt user to enter account number
                    if accountNumber == "0":
                        transact = False
                        break
                    if accountNumber in pointWorld.customers.keys():    # Check if the account number exist
                        print(
                            f"\nYour account balance is #{pointWorld.customers[accountNumber].getBalance}")
                        transact = False
                        break
                    else:
                        print("Invalid account number")
                        continue

            elif operation == "3":  # Deposit
                transact = True
                if not pointWorld.login(loginDetail):   # Check if the user is logged in
                    continue
                while transact:
                    print("\nPress 0 to cancel\n")
                    accountNumber = input("Enter your account number:  ")   # Prompt user to enter account number
                    if accountNumber == "0":
                        transact = False
                        break
                    customer = pointWorld.customers[accountNumber]  # Get the customer object
                    print("\n", customer)
                    if customer:
                        amount = int(input("Amount:  "))    # Prompt user to enter amount
                        if amount:
                            pointWorld.deposit(accountNumber, amount)   # Deposit the amount
                            print(
                                f"\nYour account has been credited with #{amount}. Your current balance is #{customer.getBalance}") # Display the current balance
                            print(
                                "\nTransaction completed and successful! Thank you for banking with us")    # Display a success message
                            transact = False    # Break out of the loop
                            break   # Break out of the loop
                        else:
                            print(
                                "Invalid amount. Transaction failed. Please try again")   # Display an error message
                            continue    # Break out of the loop
                    else:
                        print("Invalid entry. Please try again")    # Display an error message
                        continue    # Break out of the loop

            elif operation == "4":  # Withdrawal
                transact = True 
                if not pointWorld.login(loginDetail):   # Check if the user is logged in
                    continue    # Break out of the loop
                while transact:
                    print("\nPress 0 to cancel\n")  
                    accountNumber = input("Account Number:  ")  # Prompt user to enter account number
                    if accountNumber == "0":    
                        transact = False
                        break
                    customer = pointWorld.customers[accountNumber]  # Get the customer object
                    print("\n", customer)
                    if customer:
                        amount = int(input("Amount:  "))    # Prompt user to enter amount
                        if amount:  
                            pointWorld.withdrawal(accountNumber, amount)    # Withdraw the amount
                            print(
                                f"\nYour account has been debited with #{amount}. Your current balance is #{customer.getBalance}")  # Display the current balance
                            print(
                                "\nTransaction completed and successful! Thank you for banking with us")    # Display a success message
                            transact = False    # Break out of the loop
                            break   # Break out of the loop
                        else:
                            print(
                                "Invalid amount. Transaction failed. Please try again")  # Display an error message
                            continue    # Break out of the loop

            elif operation == "5":  # Transfer
                transact = True 
                if not pointWorld.login(loginDetail):   # Check if the user is logged in
                    continue    # Break out of the loop
                while transact: 
                    print("\nPress 0 to cancel\n")  
                    accountNumber = input("Account Number:  ")  # Prompt user to enter account number
                    if accountNumber == "0":    
                        transact = False    # Break out of the loop
                        break   # Break out of the loop
                    customer = pointWorld.customers[accountNumber]  # Get the customer object
                    print(customer) 
                    if customer:    
                        amount = int(input("Amount:  "))    # Prompt user to enter amount
                        if amount:  
                            pointWorld.transfer(accountNumber, amount)  # Transfer the amount
                            print(
                                f"\nYour account has been debited with #{amount}. Your current balance is #{customer.getBalance}")  # Display the current balance
                            print(
                                "\nTransaction completed and successful! Thank you for banking with us")    # Display a success message
                            transact = False    # Break out of the loop
                            break   # Break out of the loop
                        else:
                            print(
                                "Invalid amount. Transaction failed. Please try again") # Display an error message
                            continue    # Break out of the loop

            elif operation == "6":  # View transaction history
                transact = True 
                if not pointWorld.login(loginDetail):   # Check if the user is logged in
                    continue    # Break out of the loop
                while transact: 
                    userEntry = int(input("Account Number:  ")) # Prompt user to enter account number
                    customer = pointWorld.customers[accountNumber]  # Get the customer object
                    print(customer) 
                    if customer:    
                        pointWorld.viewHistory(accountNumber)   # View the transaction history
                        transact = False    # Break out of the loop
                        break   # Break out of the loop

            elif operation == "7":  # Logout
                transact = False    # Break out of the loop
                print("\nThank you for banking with us. Goodbye")   # Display a goodbye message
                break   # Break out of the loop
