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
