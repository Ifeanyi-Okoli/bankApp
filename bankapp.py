from dataclasses import dataclass
from string import digits
from datetime import datetime
import random
import uuid


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
        
    def __str__(self) -> str:
        fullName = f"{self.firstName} {self.lastName}"
        fullName = lambda first, last: first + " " + last
        return f"{fullName(self.firstName, self.lastName)} \t {self.phoneNo} \t {self.email} \t {self.gender} \t {self.dateOfBirth} \t {self.occupation} \t {self.address}"
    
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
    
    @classmethod
    def updateHistory(cls, date, type, amount):
        """Updates the transaction history of the customer"""
        accountNumber = random.choices(digits, k=10)
        cls.__setattr__("account_number", accountNumber)
        cls.history[f"{date}"] = {"type": type, "amount": amount, "balance": cls.balance}
    
    @property
    def getBalance(self):
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
    
    customers = {}
    balance: int = 0
    
    def deposit(self, account, amount):
        """Credits a customer's account"""
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
    
    def signUp(cls, firstName, lastName, phoneNo, email, gender, dateOfBirth, occupation, address):
        """signs a new customer"""
        
        customer = Customer(firstName, lastName, phoneNo, email, gender, dateOfBirth, occupation, address)
        accountNumber = customer.generateAccount()
        cls.customers[f'{accountNumber}'] = customer
        return customer
        


if __name__ == '__main__':
    running = True
    transact = False
    pointWorld = Bank()
    print("\n")
    print("WELCOME TO POINT WORLD BANK".center(60, "="))

    while running:
        print("\nPress a number between 1 and 6 that corresponds to the operation you wish to perform\n")
        operation = input("1. Sign-up \n2. Check Balance \n3. Deposit \n4. Withdrawal \n5. Transfer \n6.Transaction History \n7.Exit\n")

        if operation not in "1234567":
            print("\nWrong Entry. \nPlease enter a number between 1 and 7")
            continue
        else:
            if operation == "1":
                transact = True
                while transact:
                    print("\nThank you for choosing Point World. Please walk with me\n")
                    firstName = input("First Name:  ")
                    lastName = input("Last Name:  ")
                    phoneNo = input("Phone Number: ")
                    email = input("Email:  ")
                    dateOfBirth = input("Date of Birth:  ")
                    gender = input("Gender:  ")
                    occupation = input("Occupation: ")
                    address = input("Address:  ")
                    balance = int(input("Opening Balance (min: #1000):  "))
                    
                    try:
                        if len(firstName) > 3 and len(lastName)>3 and len(phoneNo)>3 and ("@" in email) and dateOfBirth and gender and occupation and len(address) > 3 and balance:
                            if balance >= 1000:
                                customer = Customer(firstName, lastName, phoneNo, email, gender, occupation, address, balance)
                                accountNumber = customer.generateAccount()
                                if accountNumber:
                                    pointWorld.customers.update({accountNumber: customer})
                                    # pointWorld.customers[f'{accountNumber}'] = customer
                                    print(f"\nCongratulations {firstName} {lastName}! Your account has been created successfully. Your account number is {accountNumber}. Please keep it safe")
                                    print("\n", pointWorld.customers.items())
                                    pointWorld.deposit(accountNumber, balance)
                                    print(f"\nYour account has been credited with #{balance}. Your current balance is #{customer.getBalance}")
                                    print("\nPlease login to continue")
                                    transact = False
                                    break
                                
                            else:
                                print("Opening balance must be at least #1000")
                                continue
                        else:
                            print("Invalid entry. Please try again")
                            continue
                    except ValueError:
                        print("Invalid entry")
                        break
                            
            elif operation == "2":
                transact = True
                while transact:
                    print("\nPress 0 to cancel\n")
                    accountNumber = input("Enter your account number:  ")
                    if accountNumber == "0":
                        transact = False
                        break
                    if accountNumber in pointWorld.customers.keys():
                        print(f"\nYour account balance is #{pointWorld.customers[accountNumber].getBalance}")
                        transact = False
                        break
                    else:
                        print("Invalid account number")
                        continue
                    
            elif operation == "3":
                transact = True
                while transact:
                    print("\nPress 0 to cancel\n")
                    accountNumber = input("Enter your account number:  ")
                    if accountNumber == "0":
                        transact = False
                        break
                    customer = pointWorld.customers[accountNumber]
                    print("\n",customer)
                    if customer:
                        amount = int(input("Amount:  "))
                        if amount:
                            pointWorld.deposit(accountNumber, amount)
                            print(f"\nYour account has been credited with #{amount}. Your current balance is #{customer.getBalance}")
                            print("\nTransaction completed and successful! Thank you for banking with us")
                            transact = False
                            break
                        else:
                            print("Invalid amount. Transaction failed. Please try again")
                            continue
                    else:
                        print("Invalid entry. Please try again")
                        continue
                        
            elif operation == "4":
                transact = True
                while transact:
                    print("\nPress 0 to cancel\n")
                    accountNumber = input("Account Number:  ")
                    if accountNumber == "0":
                        transact = False
                        break
                    customer = pointWorld.customers[accountNumber]
                    print("\n",customer)
                    if customer:
                        amount = int(input("Amount:  "))
                        if amount:
                            pointWorld.withdrawal(accountNumber, amount)
                            print(f"\nYour account has been debited with #{amount}. Your current balance is #{customer.getBalance}")
                            print("\nTransaction completed and successful! Thank you for banking with us")
                            transact = False
                            break
                        else:
                            print("Invalid amount. Transaction failed. Please try again")
                            continue
                        
            elif operation == "5":
                transact = True
                while transact:
                    print("\nPress 0 to cancel\n")
                    accountNumber = input("Account Number:  ")
                    if accountNumber == "0":
                        transact = False
                        break
                    customer = pointWorld.customers[accountNumber]
                    print(customer)
                    if customer:
                        amount = int(input("Amount:  "))
                        if amount:
                            pointWorld.transfer(accountNumber, amount)
                            print(f"\nYour account has been debited with #{amount}. Your current balance is #{customer.getBalance}")
                            print("\nTransaction completed and successful! Thank you for banking with us")
                            transact = False
                            break
                        else:
                            print("Invalid amount. Transaction failed. Please try again")
                            continue
                        
            elif operation == "6":
                transact = True
                while transact:
                    accountNumber = int(input("Account Number:  "))
                    customer = pointWorld.customers[accountNumber]
                    print(customer)
                    if customer:
                        pointWorld.viewHistory(accountNumber)
                        transact = False
                        break
                
                        
            elif operation == "7":
                transact = False
                print("\nThank you for banking with us. Goodbye")
                break    
            
        # break
    #     wema = Bank()

        

    #     print(str(customer))
    #     print(customer.__dict__.items())

    # chima = wema.signUp("Chima", "Okeke", "09035138223", "chima@gmail.com", "male", "13-09-1992", "Business Man", "Lagos")
    # chima.updateBalance("deposit", 1000)
    # chima.updateBalance("withdrawal", 500)
    # chima.updateBalance("deposit", 1000)

    # print(chima.getBalance)


    # print(wema.customers)















#==============================================Inheritance


class Investors(Customer):
    
    def __init__(self, firstName, lastName, phoneNo, email, address, balance=0, investment=0) -> None:
        super().__init__(firstName, lastName, phoneNo, email, address, balance)
        self.investment = investment
        
    def loan(self):
        pass
    
    def fixed(self, amount, duration = 364, rate = 0.2):
        pass
    
    def birthday(self):
        pass
    
    

# print(Investors.__dict__.items()) #prints all the attributes of the class
# print(dir(Investors)) #prints all the attributes of the class
# print("===============")
# print(dir(Customer))